class FFProbe():
    def getLength(filename):
        result = subprocess.Popen(["ffprobe", filename], stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT).stdout.readlines()
        duration_output_line = [x.decode().strip().strip('\n') for x in result if "Duration" in x.decode()]
        stream_output_line = [x.decode().strip().strip('\n') for x in result if "Stream" in x.decode()]

        for item in stream_output_line:
            if 'Video:' in item:
                for split_item in item.split(','):
                    if 'fps' in split_item:
                        fps = split_item.strip().strip('\n')

        for item in duration_output_line[0].split(','):
            if 'Duration' in item:
                duration = item.split('Duration:')[1].strip().strip('\n')

        return duration, fps
