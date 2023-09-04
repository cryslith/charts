#!/usr/bin/env python3

exec(open('../time.py').read())

data = {
    'bpm': 155,
    'guess_bpm': False,
    'bpm_notetype': 4,
    'approx_offset': 0.95,
    'notetype': 8,
    'timing_data': [2.116, 3.665, 4.826, 5.019, 5.407, 6.375, 7.923],
    'plot': True,
}

if __name__ == '__main__':
    main(**data)
