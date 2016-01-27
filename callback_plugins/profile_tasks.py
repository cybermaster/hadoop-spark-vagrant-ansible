from operator import itemgetter
import time


# Number of individual task timer items to display in summary.
# All-encompassing cummulative total will also be displayed
NUM_DISPLAY_RESULTS = 10


class CallbackModule(object):
    """
    A plugin for timing tasks

    Forked from: ansible-profile - https://github.com/jlafon/ansible-profile
    """

    def __init__(self):
        self.stats = {}
        self.current = None

    def playbook_on_task_start(self, name, is_conditional):
        """
        Logs the start of each task
        """
        if self.current is not None:
            # Record the running time of the last executed task
            self.stats[self.current] = time.time() - self.stats[self.current]

        # Record the start time of the current task
        self.current = name
        self.stats[self.current] = time.time()

    def playbook_on_stats(self, stats):
        """
        Prints the timings
        """
        # Record the timing of the very last task
        if self.current is not None:
            self.stats[self.current] = time.time() - self.stats[self.current]

        # Sort the tasks by their running time
        results = sorted(
            self.stats.items(),
            key=lambda value: value[1],
            reverse=True,
        )

        total = sum(map(itemgetter(1), results))

        # Just keep the top N for display purposes
        results = results[:NUM_DISPLAY_RESULTS]

        # Print the timings
        print "Task execution times (top {})".format(NUM_DISPLAY_RESULTS)
        for name, elapsed in results:
            print(
                "{0:-<70}{1:->9}".format(
                    '{0} '.format(name),
                    ' {0:.02f}s'.format(elapsed),
                )
            )

        # Print the total
        print(
            "{0:-<70}{1:->9}".format(
                'Total (all-inclusive) ',
                ' {0:0.2f}s'.format(total)
            )
        )