import numpy as np
import h5py
import tempfile
import os
from ligotools.readligo import *

def test_dq_channel_to_seglist_basic():
    channel = np.array([0, 0, 1, 1, 1, 0, 0, 1, 1, 1])
    segs = dq_channel_to_seglist(channel, fs = 1)

    # Checking if expected result matches received result
    expected = [slice(2, 5), slice(7, 10)]
    assert len(segs) == len(expected)
    for i in range(len(segs)):
        s, e = segs[i], expected[i]
        assert s.start == e.start and s.stop == e.stop


def test_loaddata_reads_hdf5(tmp_path):
    # Mock testing on a dummy hdf5 file
    fname = tmp_path / "test_ligo.hdf5"
    f = h5py.File(fname, "w")
    strain_grp = f.create_group("strain")
    dset = strain_grp.create_dataset("Strain", data = np.arange(5))
    dset.attrs["Xspacing"] = 1.0
    quality_grp = f.create_group("quality")
    simple = quality_grp.create_group("simple")
    simple.create_dataset("DQmask", data = np.array([1, 0, 1, 0, 1]))
    simple.create_dataset("DQShortnames", data=np.array([b"DATA", b"OTHER"]))

    inj_grp = quality_grp.create_group("injections")
    inj_grp.create_dataset("Injmask", data = np.array([0, 0, 1, 0, 0]))
    inj_grp.create_dataset("InjShortnames", data = np.array([b"INJ"]))

    meta = f.create_group("meta")
    meta.create_dataset("GPSstart", data = 1000000000)

    strain, time, dq = loaddata(str(fname), ifo = "H1")

    assert len(strain) == 5
    assert "DATA" in dq
    assert "INJ" in dq
    assert np.allclose(time[0], 1000000000)