import tracemalloc
import time
import numpy as np
import random
import argparse
import matplotlib.pyplot as plt
import naive_search
import boyer_moore

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text_range',
                        type=int,
                        required=True,
                        nargs=3,
                        help='Text size range (min max increment)')
    parser.add_argument('--pattern_range',
                        type=int,
                        required=True,
                        nargs=3,
                        help='Pattern size range (min max increment)')
    parser.add_argument('--rounds',
                        type=int,
                        default=10,
                        help='Number of rounds to run each algorithm ' \
                             + '(default: 10)')
    parser.add_argument('--out_file',
                        type=str,
                        required=True,
                        help='File to save plot to')
    parser.add_argument('--width',
                        type=float,
                        default=8,
                        help='Width of plot in inches (default: 8)')
    parser.add_argument('--height',
                        type=float,
                        default=5,
                        help='Height of plot in inches (default: 5)')
    return parser.parse_args()

def get_random_string(alphabet, length):
    return ''.join(random.choice(alphabet) for i in range(length))

def get_random_substring(string, length):
    if length > len(string):
        raise ValueError("Length of substring is longer than the string.")

    start_index = random.randint(0, len(string) - length)
    return string[start_index:start_index + length]

def run_test(test_function, T, P):
    start = time.monotonic_ns()
    r = test_function(T, P)
    stop = time.monotonic_ns()

    tracemalloc.start()
    r = test_function(T, P)
    mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return stop - start, mem[1] - mem[0]

def test_harness(test_functions,
                 text_size_range,
                 pattern_size_range,
                 rounds):
    run_times = [ [] for _ in range(len(test_functions))]
    mem_usages = [ [] for _ in range(len(test_functions))]
    
    for j, test_function in enumerate(test_functions):
        for pattern_size in pattern_size_range:
            text_run_times = []
            text_mem_usages = []
            for text_size in text_size_range:
                _run_times = []
                _mem_usages = []

                for _ in range(rounds):
                    T = get_random_string(['A', 'C', 'T', 'G'], text_size)
                    P = get_random_substring(T, pattern_size)

                    run_time, mem_usage = run_test(test_function, T, P)
                    _run_times.append(run_time)
                    _mem_usages.append(mem_usage)

                text_run_times.append(np.mean(_run_times))
                text_mem_usages.append(np.mean(_mem_usages))
            run_times[j].append(text_run_times)
            mem_usages[j].append(text_mem_usages)
    
    return run_times, mem_usages

def main():
    args = get_args()

    text_size_range =  range(args.text_range[0],
                             args.text_range[1],
                             args.text_range[2])
    
    pattern_size_range = range(args.pattern_range[0],
                               args.pattern_range[1],
                               args.pattern_range[2])

    test_functions = [naive_search.naive_search, boyer_moore.boyer_moore_search]
    function_names = ['Naive', 'Boyer-Moore']
    function_colors = ['blue', 'red']

    pattern_size_opacity = lambda pattern_size: (pattern_size - args.pattern_range[0])/(args.pattern_range[1]-args.pattern_range[0])*0.6 + 0.2


    run_times, mem_usages = test_harness(test_functions,
                                         text_size_range,
                                         pattern_size_range,
                                         args.rounds)

    fig, axs = plt.subplots(2,1, figsize=(args.width, args.height))
    ax = axs[0]
    for i, function_name in enumerate(function_names):
        for j, pattern_size in enumerate(pattern_size_range):
            ax.plot(text_size_range, run_times[i][j], label=f'{function_name} @ |P|={pattern_size}', color=(function_colors[i], pattern_size_opacity(pattern_size)))
    ax.set_title(f'String Search Performance')
    ax.set_xlabel('Text size')
    ax.set_ylabel('Run time (ns)')
    ax.legend(loc='best', frameon=False, ncol=3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax = axs[1]
    for i, function_name in enumerate(function_names):
        for j, pattern_size in enumerate(pattern_size_range):
            ax.plot(text_size_range, mem_usages[i][j], label=f'{function_name} @ |P|={pattern_size}', color=(function_colors[i], pattern_size_opacity(pattern_size)))
    ax.set_xlabel('Text size')
    ax.set_ylabel('Memory (bytes)')
    ax.legend(loc='best', frameon=False, ncol=3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()

    plt.savefig(args.out_file)

if __name__ == '__main__':
    main()
