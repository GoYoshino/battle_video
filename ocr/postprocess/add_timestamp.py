from typing import Dict, List


def __slice_timestamp(timestamps: List[int], blocks_per_image: int) -> List[int]:
    if len(timestamps) <= blocks_per_image:
        return timestamps
    return timestamps[blocks_per_image:]

def add_timestamp(segmented_text_chunks: List[Dict[int, str]], timestamps:List[int], blocks_per_image: int):
    timestamped: Dict[int, str] = {}

    for text_chunk in segmented_text_chunks:
        for index, text in text_chunk.items():
            target_timestamp = timestamps[index]
            timestamped[target_timestamp] = text
        timestamps = __slice_timestamp(timestamps, blocks_per_image)

    return timestamped
