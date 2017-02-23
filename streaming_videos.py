import sys

CACHE_SIZE = 0


class Video:

  _id = None
  _size = None

  def __init__(self, the_id, size):
    self._id = the_id
    self._size = size

  def __str__(self):
    return "id: {} size: {}".format(self._id, self._size)


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
    self._videos = []

  def get_optimal_videos(self, video_weights_matrix):
    no_videos = len(video_weights_matrix)
    valueMatrix = [[] for _ in no_videos]
    valueMatrix[0] = [0 for _ in no_videos]
    keep = [[0 for _ in CACHE_SIZE] for _ in no_videos]
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
    k = CACHE_SIZE
    for i in range(no_videos, 0, -1):
      if keep[i][k] == 1:
        videos.append(video_weights_matrix[i])
        k -= video_weights_matrix[i][1]
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
  CACHE_SIZE = int(line[4])
  # Read endpoints and latencies
  endpoints = []
  # Assign caches
  caches = [Cache(i) for i in range(no_caches)]
  # Read videos
  video_sizes = input_file.readline().split(' ')
  videos = [Video(i, elem) for i, elem in enumerate(video_sizes)]
  for i in range(no_endpoints):
    line = input_file.readline().split(' ')
    # New endpoint, give id and datacenter latency
    endpoints.append(Endpoint(i, line[0]))
    for _ in range(int(line[1])):
      line2 = input_file.readline().split(' ')
      endpoints[-1]._caches.append((caches[int(line2[0])], int(line2[1])))
      caches[int(line2[0])]._endpoints.append(endpoints[-1])
  # Read requests
  for _ in range(no_requests):
    line = input_file.readline().split(' ')
    endpoints[int(line[1])]._videos.append((videos[int(line[0])],
                                           int(line[2])))
  # Print shit
  print([str(video) for video in videos])
  print("__________________________")
  print([str(endpoint) for endpoint in endpoints])
  print("__________________________")
  print([str(cache) for cache in caches])
