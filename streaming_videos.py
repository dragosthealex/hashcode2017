import sys
import time


CACHE_SIZE = 0


class Video:

  _id = None
  _size = None

  def __init__(self, the_id, size):
    self._id = the_id
    self._size = size

  def __str__(self):
    return "id: {} size: {}".format(self._id, self._size)

  def __hash__(self):
    return self._id


class Endpoint:

    _id = None
    _latency = None
    _caches = None
    _videos = None

    def __init__(self, the_id, latency):
      self._id = the_id
      self._latency = latency
      self._caches = []
      self._videos = []

    def __str__(self):
      return ("id: {} latency: {} caches: " +
              "{} videos: {}").format(self._id, self._latency,
                                      [str(cache) for cache in self._caches],
                                      [str(video) for video in self._videos])


class Cache:

  _id = None
  _endpoints = None
  _videos = None
  _avg_latencies = None

  def __init__(self, the_id):
    self._id = the_id
    self._endpoints = []
    self._videos = {}

  def get_optimal_videos(self, video_weights_matrix=None):
    start = time.clock()
    video_weights_matrix = self._videos
    no_videos = len(video_weights_matrix)
    print "PROCESSING CACHE: " + str(self._id) + " with " + str(no_videos) + "v"
    valueMatrix = [[0 for _ in range(CACHE_SIZE)] for _ in range(no_videos)]
    keep = [[0 for _ in range(CACHE_SIZE)] for _ in range(no_videos)]
    for i, video in enumerate(video_weights_matrix):
      for j in range(CACHE_SIZE):
        # If video's weight less than current weight limit
        # we either have the same value as when we could use prev videos,
        # or we add the video, but subtract its weight
        if(video[0] <= j):
          if valueMatrix[i - 1][j] <= video[1] + \
             valueMatrix[i - 1][j - video[0]]:
            valueMatrix[i][j] = video[1] + valueMatrix[i - 1][j - video[0]]
            keep[i][j] = 1
          else:
            valueMatrix[i][j] = valueMatrix[i - 1][j]
        else:
          valueMatrix[i][j] = valueMatrix[i - 1][j]
    videos = []
    k = CACHE_SIZE - 1
    for i in range(no_videos - 1, -1, -1):
      if keep[i][k] == 1:
        videos.append(video_weights_matrix[i])
        k -= video_weights_matrix[i][0]
    print "Time: " + str(time.clock() - start)
    return videos

  def __str__(self):
    return ("id: {} endpoints: {} videos: " +
            "{} latencies: {}").format(self._id,
                                       [str(ept) for ept in self._endpoints],
                                       [str(video) for video in self._videos],
                                       self._avg_latencies)


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("You should give a file name as parameter.")
    sys.exit()
  # Open input file
  input_name = sys.argv[1]
  input_file = open(input_name, 'r')
  # Read first line
  line = input_file.readline().split(' ')
  no_videos = int(line[0])
  no_endpoints = int(line[1])
  no_requests = int(line[2])
  no_caches = int(line[3])
  print "CACHES: #" + str(no_caches)
  CACHE_SIZE = int(line[4])
  # Read endpoints and latencies
  endpoints = []
  # Assign caches
  caches = [Cache(i) for i in range(no_caches)]
  # Read videos
  video_sizes = input_file.readline().split(' ')
  videos = [Video(i, int(elem)) for i, elem in enumerate(video_sizes)]
  for i in range(no_endpoints):
    line = input_file.readline().split(' ')
    # New endpoint, give id and datacenter latency
    endpoints.append(Endpoint(i, int(line[0])))
    for _ in range(int(line[1])):
      line2 = input_file.readline().split(' ')
      endpoints[-1]._caches.append((caches[int(line2[0])], int(line2[1])))
      caches[int(line2[0])]._endpoints.append(endpoints[-1])
  # Read requests
  for _ in range(no_requests):
    line = input_file.readline().split(' ')
    video = videos[int(line[0])]
    endpoint = endpoints[int(line[1])]
    requests = int(line[2])

    for cache, latency_to_cache in endpoint._caches:
      latency_saved = endpoint._latency - latency_to_cache
      value = latency_saved * requests
      if video in cache._videos:
        cache._videos[video] = (video._size, value + cache._videos[video][1],
                                video._id)
      else:
        cache._videos[video] = (video._size, value, video._id)
  for cache in caches:
    cache._videos = cache._videos.values()

  no_used_caches = 0
  output = ''
  for cache in caches:
    videos = cache.get_optimal_videos()
    if len(videos) == 0:
      continue
    no_used_caches += 1
    res = str(cache._id)
    for vid in videos:
      res += ' ' + str(vid[2])
    res += '\n'
    output += res
  print(no_used_caches)
  print(output.strip())
