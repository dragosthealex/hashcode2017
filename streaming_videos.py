import sys

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
  # Read videos
  videos = input_file.readline().split(' ')
  # Read endpoints and latencies
  endpoints = []
  for _ in range(no_endpoints):
    line = input_file.readline().split(' ')
    endpoints.append({'data_center': int(line[0]), 'caches': []})
    for _ in range(int(line[1])):
      line = input_file.readline().split(' ')
      (endpoints[-1]['caches']).append({'id': line[0], 'latency': line[1]})
  # Read requests
  requests = []
  for _ in range(no_requests):
    line = input_file.readline().split(' ')
    requests.append({'video': line[0], 'endpoint': line[1], 'no': line[2]})
