import kagglehub

# Download latest version
path = kagglehub.dataset_download("nikitatkachenko/19332-spotify-songs")

print("Path to dataset files:", path)