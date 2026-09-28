"""Recompute internal diagnostics; this does not validate geographic accuracy."""
import json
from pathlib import Path
import numpy as np

d = json.loads(Path(__file__).with_name('qumran_aerial_trial.json').read_text())
a = np.asarray(d['source_pixels'], dtype=float)
b = np.asarray(d['destination_pixels'], dtype=float)
m = np.asarray(d['source_to_mosaic_affine'], dtype=float)
keep = np.asarray(d['inliers'], dtype=bool).ravel()
x = np.column_stack((a[keep], np.ones(keep.sum())))
y = b[keep]
rmse = np.sqrt(np.mean(np.sum((x @ m.T - y) ** 2, axis=1)))
loo = []
for i in range(len(x)):
    use = np.arange(len(x)) != i
    fit = np.linalg.lstsq(x[use], y[use], rcond=None)[0]
    loo.append(float(np.linalg.norm(x[i] @ fit - y[i])))
assert d['status'] == 'rejected_for_feature_geometry'
assert abs(rmse - d['training_rmse_pixels']) < 1e-6
assert np.allclose(loo, d['leave_one_out_pixels'])
print(json.dumps({'tentative_pairs':len(a), 'inliers':int(keep.sum()),
                  'training_rmse_pixels':float(rmse),
                  'leave_one_out_pixels':loo,
                  'independent_check_points':0,
                  'geometry_approved':False}, indent=2))
