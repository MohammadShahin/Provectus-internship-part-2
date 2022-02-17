
def filter_content(old_content):
    new_content = ','.join(old_content)
    new_content = new_content.split(',')
    edited_content = []
    for item in new_content:
        edited_content += item.split()
    edited_content = [val for val in edited_content if len(val) != 0]
    return edited_content


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
