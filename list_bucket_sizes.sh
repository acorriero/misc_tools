#!/usr/bin/bash

set +x

# Enter the number of days ago to collect the metric
days_ago=2

period=$((3600*24*days_ago))

function convert_size() {
  size=$1
  # If bucket is empty, return 0B
  if ! [[ $size =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    echo "0B"
    return
  fi
  # Convert to human-readable format
  units=("B" "KB" "MB" "GB" "TB")
  for ((i=0; i<${#units[@]}-1; i++)); do
    if (( $(echo "$size<1024" | bc -l) )); then
      break
    fi
    size=$(echo "scale=2; $size/1024" | bc)
  done
  # Round to whole number and print
  size=$(printf "%.0f" $size)
  echo "$size${units[i]}"
}

function calcs3bucketsize() {
  # Accepts a list of S3 buckets as arguments
  for bucket in "$@"; do
    sizeInBytes=$(
      aws cloudwatch get-metric-statistics \
        --namespace AWS/S3 \
        --metric-name BucketSizeBytes \
        --dimensions Name=BucketName,Value="$bucket" Name=StorageType,Value=StandardStorage \
        --start-time $(($(date +%s) - ${period})) \
        --end-time $(date +%s) \
        --period ${period} \
        --statistics Sum \
        --region us-east-1 \
        --output text | tail -1 | awk '{print $2}'
    )
    sizeInBytes=$(convert_size $sizeInBytes)
    # Output for csv
    echo -e "${sizeInBytes},${bucket}"
  done | sort -hr
}

# Get list of buckets
buckets=$(aws s3 ls | awk '{print $3}')

# Convert list of buckets to array
buckets_array=($buckets)

# Send array and redirect output to a CSV file
calcs3bucketsize "${buckets_array[@]}" > allregions-buckets-s3-sizes.csv
