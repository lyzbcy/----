import sys

class SentinelSolver:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.min_guards = m * n + 1
        self.solution_count = 0
        # 0: empty, 1: guard, 2: covered
        # To track coverage efficiently, we can use a separate coverage grid or count.
        # But for pruning, we need to know specific cell coverage.
        # Let's use a grid where integer value indicates how many guards cover it.
        self.covered = [[0] * n for _ in range(m)]
        self.guards = [[0] * n for _ in range(m)]
        
    def is_valid(self, r, c):
        return 0 <= r < self.m and 0 <= c < self.n

    def add_guard(self, r, c):
        self.guards[r][c] = 1
        # Mark coverage
        dirs = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                self.covered[nr][nc] += 1

    def remove_guard(self, r, c):
        self.guards[r][c] = 0
        # Unmark coverage
        dirs = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                self.covered[nr][nc] -= 1

    def solve(self, idx, count):
        # Pruning 1: Current count already exceeds or equals best found (if we just want one best, strictly greater. If we want all, equals is okay? No, we want min guards.)
        # If count >= self.min_guards, we can stop if we only want one optimal. 
        # But we need "number of optimal solutions". So if count > self.min_guards, return.
        if count > self.min_guards:
            return

        if idx == self.m * self.n:
            # Check if all covered
            all_covered = True
            for r in range(self.m):
                for c in range(self.n):
                    if self.covered[r][c] == 0:
                        all_covered = False
                        break
                if not all_covered: break
            
            if all_covered:
                if count < self.min_guards:
                    self.min_guards = count
                    self.solution_count = 1
                elif count == self.min_guards:
                    self.solution_count += 1
            return

        r, c = divmod(idx, self.n)

        # Pruning 2: Check (r-1, c). If it's not covered, we MUST place a guard at (r, c) or (r-1, c+1)...
        # Actually, the only future cell that can cover (r-1, c) is (r, c).
        # (r+1, c) covers (r, c). (r, c+1) covers (r, c).
        # Wait, who covers (r-1, c)?
        # Neighbors of (r-1, c): (r-1, c), (r-2, c), (r-1, c-1), (r-1, c+1), (r, c).
        # Cells processed so far: all < (r, c).
        # (r-2, c) is long gone. (r-1, c-1) is gone. (r-1, c) is gone. (r-1, c+1) is gone?
        # Wait, if we are at (r, c), we are visiting row by row.
        # Previous row is r-1.
        # When we are at (r, c), can we still cover (r-1, c)?
        # Yes, placing a guard at (r, c) covers (r-1, c).
        # Can any FUTURE cell ( > (r, c)) cover (r-1, c)?
        # Future cells are (r, c+1)... and rows r+1...
        # (r, c+1) covers (r-1, c+1), not (r-1, c).
        # (r+1, c) covers (r, c), not (r-1, c).
        # So (r, c) is indeed the LAST cell that can cover (r-1, c).
        
        # So, if we are at (r, c), check (r-1, c).
        # If (r-1, c) is NOT covered, we MUST place a guard at (r, c).
        # If we don't, (r-1, c) will remain uncovered forever.
        
        must_place = False
        if r > 0:
            if self.covered[r-1][c] == 0:
                must_place = True
        
        # Try placing guard
        if count + 1 <= self.min_guards: # Optimization
            self.add_guard(r, c)
            self.solve(idx + 1, count + 1)
            self.remove_guard(r, c)

        # Try NOT placing guard
        # Only allowed if not forced to place
        if not must_place:
            self.solve(idx + 1, count)

def main():
    if len(sys.argv) >= 3:
        m, n = int(sys.argv[1]), int(sys.argv[2])
    else:
        # Default or read from stdin
        line = sys.stdin.readline()
        if not line:
            return
        parts = list(map(int, line.split()))
        if len(parts) == 2:
            m, n = parts
        else:
            return

    solver = SentinelSolver(m, n)
    solver.solve(0, 0)
    print(f"{solver.min_guards}")
    print(f"{solver.solution_count}")

if __name__ == "__main__":
    main()
