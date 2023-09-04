#!/usr/bin/env python3

'''Calculate BPM and offset by averaging the timing information from several sampled notes'''

from heapq import heappush, heappop
from numpy.linalg import lstsq

def main(bpm, guess_bpm, bpm_notetype, approx_offset, notetype, timing_data, plot):
    '''
    bpm: your guess for the bpm
    guess_bpm: true: try to guess the bpm. false: assume the above is correct.
    bpm_notetype: note type (e.g. quarter notes = 4) of the beat the bpm is measured in
    approx_offset: your guess for what the offset should be in seconds
    notetype: most granular note type (e.g. eighth notes = 8) of the samples in timing_data
    timing_data:
    measured timings of notes in seconds,
    optionally with integer beat counts of notes
    (measured in bpm_notetype), otherwise will be guessed
    '''
    if notetype % bpm_notetype != 0:
        raise ValueError
    nps = bpm*notetype/bpm_notetype/60
    times, given_notecounts = cleanup_timing_data(timing_data)
    notecounts = guess_notecounts(times, given_notecounts, nps)
    (best_nps, b) = regress(times, notecounts, None if guess_bpm else nps)
    best_offset = offset(best_nps, b, approx_offset)
    print(f'bpm: {best_nps*60*bpm_notetype/notetype}')
    print(f'null offset: {best_offset}')
    print(f'ITG offset: {best_offset + 0.009}')
    if plot:
        draw_plot(times, notecounts, best_nps, b, bpm_notetype, notetype)


def cleanup_timing_data(timing_data):
    times = [x if type(x) == tuple else (x, None) for x in timing_data]
    times.sort()
    given_notecounts = [y for (x, y) in times]
    times = [x for (x, y) in times]
    given_notecounts = [None if y is None else y * notetype // bpm_notetype for y in given_notecounts]
    return (times, given_notecounts)


def guess_notecounts(times, given_notecounts, nps):
    def correct(kx, ky, x):
        return round(ky + nps*(x - kx))

    output = [None for _ in times]

    seen = set()
    frontier = []
    for (i, y) in enumerate(given_notecounts):
        if y is None:
            continue
        heappush(frontier, (0, i, y))
    if all(x is None for x in given_notecounts):
        heappush(frontier, (0, 0, 0))
    while frontier:
        (_, i, y) = heappop(frontier)
        x = times[i]
        if i in seen:
            continue
        seen.add(i)
        output[i] = y
        if i > 0:
            heappush(frontier, (x - times[i-1], i-1, correct(x, y, times[i-1])))
        if i < len(times) - 1:
            heappush(frontier, (times[i+1] - x, i+1, correct(x, y, times[i+1])))
    return output


def regress(times, notecounts, nps=None):
    '''
    calculate (nps, b) such that
    notecount = nps*time + b
    if nps is not None then use that nps instead of regressing it
    '''
    if nps is None:
        (result, residuals, _, _) = lstsq([[x, 1] for x in times], notecounts, rcond=None)
        nps = result[0]
        b = result[1]
    else:
        (result, residuals, _, _) = lstsq([[1] for _ in times], [y - nps*x for (x, y) in zip(times, notecounts)], rcond=None)
        b = result[0]
    return (nps, b)


def offset(nps, b, approx_offset):
    return (b - round(b - approx_offset*nps))/nps


def draw_plot(times, notecounts, nps, b, bpm_notetype, notetype):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2)
    beatcounts = [x * bpm_notetype / notetype for x in notecounts]

    axs[0].plot(beatcounts, [(x - b)/nps for x in notecounts])
    axs[0].plot(beatcounts, times, 'r+')

    axs[1].plot(beatcounts, [0]*len(beatcounts))
    axs[1].plot(beatcounts, [y - (x - b)/nps for (x, y) in zip(notecounts, times)], 'r+')
    plt.show()
