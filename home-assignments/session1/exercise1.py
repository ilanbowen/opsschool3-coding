import sys
import json
import yaml


def main():
    with open(sys.argv[1]) as json_data:
        data = json.load(json_data)
        ppl_ages = (data["ppl_ages"])
        buckets = data["buckets"]
        buckets_length = len(buckets)
        sorted_buckets = sorted(buckets, key=int)

    nameslist_outputfile = 'nameslist.yml'
    index = 0
    open(nameslist_outputfile, 'w')
    fitsinbucketdict = {}

    while index < buckets_length - 1:
        yamldata = []
        incremented_key_index = (index + 1)
        bottom_partition_key = sorted_buckets[index]
        upper_partition_key = sorted_buckets[incremented_key_index]
        index += 1
        agerange = str(bottom_partition_key) + "-" + str(upper_partition_key)

        for name, age in ppl_ages.items():
            if bottom_partition_key <= age < upper_partition_key:
                raw_unicode = (name.encode('raw_unicode_escape'))
                name1 = name.encode('utf-8')
                if name == raw_unicode:
                    yamldata.append(name1)
                else:
                    yamldata.append(name)
                fitsinbucketdict[name] = age

        with open(nameslist_outputfile, 'a') as outfile:
            yaml.dump({agerange: yamldata}, outfile, allow_unicode=True, default_flow_style=False)

    all(map(ppl_ages.pop, fitsinbucketdict))  # use all() so it works for Python 2 and 3.
    ppl_ages_key_max = max(ppl_ages.keys(), key=(lambda k: ppl_ages[k]))
    oldest_age = ppl_ages.get(ppl_ages_key_max)
    highest_bucket_number = max(buckets)

    agerange = str(highest_bucket_number) + "-" + str(oldest_age)

    yamldata = []

    for name, age in ppl_ages.items():
        raw_unicode = (name.encode('raw_unicode_escape'))
        name1 = name.encode('utf-8')
        if name == raw_unicode:
            yamldata.append(name1)
        else:
            yamldata.append(name)

    with open(nameslist_outputfile, 'a') as outfile:
        yaml.dump({agerange: yamldata}, outfile, allow_unicode=True, default_flow_style=False)


if __name__ == "__main__":
    main()
