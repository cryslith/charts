#!/usr/bin/env python3

# Calculate an offset by averaging the timing information from several sampled notes

bpm = 155
bpm_notetype = 4 # note type (e.g. quarter notes = 4) of the beat the bpm is measured in
approx_offset = 0.95 # your guess for what the offset should be in seconds

notetype = 8 # most granular note type (e.g. eighth notes = 8) of the samples below
nps = bpm*notetype/bpm_notetype/60

times = [2.116, 3.665, 4.826, 5.019, 5.407, 6.375, 7.923] # measured timings of notes in seconds

def closest(nps, approx_offset, time):
    n = round((time - approx_offset)*nps)
    return time - n/nps

def best_offset(nps, approx_offset, times):
    return sum(closest(nps, approx_offset, t) for t in times)/len(times)

print(nps, 1/nps)
print([closest(nps, approx_offset, t) for t in times])

def main():
    offset = best_offset(nps, approx_offset, times)
    print(f'null offset: {offset}')
    print(f'ITG offset: {offset + 0.009}')
if __name__ == '__main__':
    main()
