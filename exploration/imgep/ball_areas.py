import bisect

class BallCloud1D:
    def __init__(self, r):
        self.r = r
        self.intervals = []  # list of disjoint [start, end) intervals
        self.total_length = 0.0

    def add_point(self, x):
        new_start, new_end = x - self.r, x + self.r
        intervals = self.intervals
        i = bisect.bisect_left(intervals, (new_start, new_end))

        # Merge with overlapping intervals
        merged_start, merged_end = new_start, new_end
        remove = []

        # Check interval to the left
        if i > 0 and intervals[i-1][1] >= new_start:
            i -= 1

        while i < len(intervals) and intervals[i][0] <= new_end:
            s, e = intervals[i]
            merged_start = min(merged_start, s)
            merged_end = max(merged_end, e)
            self.total_length -= e - s  # remove their contribution
            remove.append(i)
            i += 1

        # Remove merged intervals
        for j in reversed(remove):
            intervals.pop(j)

        # Insert merged interval
        bisect.insort(intervals, (merged_start, merged_end))
        self.total_length += merged_end - merged_start

    def get_total_length(self):
        return self.total_length
