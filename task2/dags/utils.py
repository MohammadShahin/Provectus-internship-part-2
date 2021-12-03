

def filter_content(old_content):
    new_content = old_content.replace('\n', ',')
    new_content = new_content.replace(',', ' ')
    new_content = new_content.split()
    final_content = []
    for item in new_content:
        final_item = [char for char in item if char.isalpha()]
        final_item = ''.join(final_item)
        final_content.append(final_item)
    final_content = [val for val in final_content if len(val) != 0]
    return final_content


def split_list(org_list, num_partitions):
    assert num_partitions > 0
    if num_partitions == 1:
        return [org_list]
    partition_length = len(org_list) // num_partitions
    partitions = [org_list[:partition_length]]
    for i in range(1, num_partitions - 1):
        partitions.append(org_list[partition_length * i: partition_length * (i + 1)])
    partitions.append(org_list[partition_length * (num_partitions - 1):])
    return partitions
