from hyperminhash import HyperMinHash
import sys

seed = 'a'
n_keys = 1 << 20
mod = 999
ratio = 0.001

index_bits = 16
minhash_bits = 16

hll = HyperMinHash(index_bits, 6, 0)
hll_small = HyperMinHash(index_bits, 6, 0)

hmh = HyperMinHash(index_bits, 6, minhash_bits)
hmh_small = HyperMinHash(index_bits, 6, minhash_bits)


def calc_error(estimate, expected):
    if (estimate > expected):
        return 100 * (estimate - expected) / expected

    return 100 * (expected - estimate) / expected


print("seed {} n_keys {} mod {} ratio {} index_bits {} minhash_bits {}".format(
    seed, n_keys, mod, ratio, index_bits, minhash_bits))

for i in range(1, n_keys + 1):
    if i & (i - 1) == 0:
        target = i * ratio

        try:
            hll_count = hll.count()
            hll_small_count = hll_small.count()
            hll_intersect_count = hll.intersection(hll_small)[0]
            hll_error = calc_error(hll_intersect_count, target)

            hmh_count = hmh.count()
            hmh_small_count = hmh_small.count()
            hmh_intersect_count = hmh.intersection(hmh_small)[0]
            hmh_error = calc_error(hmh_intersect_count, target)

            print("hll - count ({:10.0f} {:10.0f} {:10.0f}) intersect {:10.0f} target {:10.0f} error {:3.3f}".format(
                i, hll_count, hll_small_count, hll_intersect_count, target,
                hll_error))
            print("hmh - count ({:10.0f} {:10.0f} {:10.0f}) intersect {:10.0f} target {:10.0f} error {:3.3f}".format(
                i, hmh_count, hmh_small_count, hmh_intersect_count, target,
                hmh_error))
            sys.stdout.flush()
        except ValueError:  # ignore nan case
            pass

    key = "{}|{}".format(seed, i)
    hll.update([key])
    hmh.update([key])

    if i % mod == 0:
        hll_small.update([key])
        hmh_small.update([key])

print("DONE")
