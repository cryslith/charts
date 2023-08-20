#!/usr/bin/env python3

'''Calculate BPM and offset by averaging the timing information from several sampled notes'''

from heapq import heappush, heappop
from numpy.linalg import lstsq

bpm = 93.15 # your guess for the bpm
guess_bpm = False # true: try to guess the bpm. false: assume the above is correct.
bpm_notetype = 4 # note type (e.g. quarter notes = 4) of the beat the bpm is measured in
approx_offset = 0.65 # your guess for what the offset should be in seconds

notetype = 8 # most granular note type (e.g. eighth notes = 8) of the samples below
if notetype % bpm_notetype != 0:
    raise ValueError
nps = bpm*notetype/bpm_notetype/60

# measured timings of notes in seconds
# optionally with integer beat counts of notes (measured in bpm_notetype), otherwise will be guessed
times = [
    # (1.921, 4),
    # 2.554,
    # 3.827,
    # 4.468,
    # (5.121, 9),
    # 8.994,
    # 10.279,
    # 11.566,
    # 12.199,
    # 12.847,
    # (38.618, 61),
    # (39.588, 62.5),
    # 25.729,
    # 23.167,
    ## cut
    # (42.389, 67),
    # 44.974,
    # 46.259,
    # (52.7, 83),
    # 59.128,
    # 60.420,
    # 63.008,
    # 63.648,
    # 73.319,
    # 74.609,
    # (77.165, 121),
    # 80.057,
    ## cut
    # (82.929, 130),
    # 83.553,
    # 85.497,
    # 86.159,
]
times = [x if type(x) == tuple else (x, None) for x in times]
times.sort()
given_notecounts = [y for (x, y) in times]
times = [x for (x, y) in times]
given_notecounts = [None if y is None else y * notetype // bpm_notetype for y in given_notecounts]


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
    if not given_notecounts:
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


# calculate (nps, b) such that
# notecount = nps*time + b
# if nps is not None then use that nps instead of regressing it
def regress(times, notecounts, nps=None):
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

def plot(times, notecounts, nps, b):
    import matplotlib.pyplot as plt
    beatcounts = [x * bpm_notetype / notetype for x in notecounts]
    fig, axs = plt.subplots(2)

    axs[0].plot(beatcounts, [(x - b)/nps for x in notecounts])
    axs[0].plot(beatcounts, times, 'r+')

    axs[1].plot(beatcounts, [0]*len(beatcounts))
    axs[1].plot(beatcounts, [y - (x - b)/nps for (x, y) in zip(notecounts, times)], 'r+')
    plt.show()

def main():
    notecounts = guess_notecounts(times, given_notecounts, nps)
    (best_nps, b) = regress(times, notecounts, None if guess_bpm else nps)
    best_offset = offset(best_nps, b, approx_offset)
    print(f'bpm: {best_nps*60*bpm_notetype/notetype}')
    print(f'null offset: {best_offset}')
    print(f'ITG offset: {best_offset + 0.009}')
    plot(times, notecounts, best_nps, b)
if __name__ == '__main__':
    main()
