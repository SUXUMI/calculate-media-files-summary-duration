import os
import subprocess
import datetime
import sys


class MediaFilesSummaryDurationCalculator:
    def get_files_list(self, dir):
        """Get full list of files in directory recursively"""

        paths = []
        paths = [os.path.join(dp, f) for dp, dn,
                 filenames in os.walk(dir) for f in filenames]

        return paths

    def get_duration_cmd(self, filepath) -> str:
        """Prepare CMD for detecting the file duration"""

        cmd = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{}"'.format(filepath)

        return cmd

    def get_file_duration(self, filepath) -> float:
        """Try to get single file duration"""

        seconds = 0.

        cmd = self.get_duration_cmd(filepath)

        process = subprocess.run(cmd, shell=True, capture_output=True)

        # ignore when file is no in valid format or is not accessible/readable
        if (not process.stderr):
            try:
                seconds = float(process.stdout.decode("utf-8"))
            except:
                pass

        return seconds

    def get_summary_duration(self, files) -> float:
        """Get files summary duration in seconds"""

        summary = 0.

        files = self.get_files_list(dir)

        for file in files:
            summary += self.get_file_duration(file)

        return summary

    def get_summary_duration_formatted(self, dir):
        """Get formatted files summary duration"""
        
        duration = int(self.get_summary_duration(dir))

        return str(datetime.timedelta(seconds=duration))


dir = os.getcwd()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dir = sys.argv[1]

print("Files summary duration: ", (MediaFilesSummaryDurationCalculator()).get_summary_duration_formatted(dir))
