from common_utils.logger import stream, logger
import cProfile
import pstats


def find_nth(string, substring, n):
    if n == 1:
        return string.find(substring)
    elif n == 2:
        return string.find(substring, string.find(substring) + 1)
    else:
        return string.find(substring, find_nth(string, substring, n - 1) + 1)


def time_profile(func):
    """ Decorator for profiling the execution of a function """

    def wrapper(*args, **kwargs):
        prof = cProfile.Profile()
        prof.enable()
        ret_val = prof.runcall(func, *args, **kwargs)
        prof.disable()
        logger.debug("Printing time profile...")
        ps = pstats.Stats(prof, stream=stream)
        ps.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(30)
        return ret_val

    return wrapper
