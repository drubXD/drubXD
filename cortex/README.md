# Cortex — Brain Explorer

A deployable browser-only MRI viewer with a dark Poppins interface, a human cortical reference mesh, interactive highlighted region, local NIfTI volume previews, intensity slices, threshold controls, transparency, rotation, and PNG export.

## Run

Requires Node.js 22 or newer. No package installation or build step is required. Fonts, meshes and Three.js are bundled locally.

    node server.mjs

Open http://127.0.0.1:4173. Change the port with the PORT environment variable.

## Verify

    node --check dist/app.js
    node --check dist/nifti.js
    node --test tests/nifti.test.mjs

Generate a synthetic, non-patient ellipsoid volume for manual upload checks:

    node tests/fixture.mjs

Use tests/phantom.nii or tests/phantom.nii.gz. tests/invalid.nii exercises the error state. This fixture is intentionally not a real brain or a clinical dataset.

## Deploy

Serve the contents of dist/ with any static host over HTTPS. No server API, secrets, database, CDN access, or external font service is needed. The .openai/hosting.json manifest identifies the existing private Sites deployment. Keep its project_id unchanged for updates.

The included server is for local development, not production. No build or package installation is necessary. The package.json scripts are optional shortcuts if npm is installed.

## Supported imaging

- NIfTI-1 single-file .nii and .nii.gz, three-dimensional volumes only.
- uint8, int8, int16, uint16, int32, uint32, float32 and float64 voxels; both byte orders; slope/intercept intensity scaling.
- Input limit 100 MB, gzip expansion limit 200 MB; max 1024 voxels per axis.
- Approximately 130,000 sampled voxels in the 3D threshold preview; slices use the original intensity data.
- Stored voxel axes and spacing are preserved. The affine is not applied: anatomical orientation labels are deliberately omitted.
- DICOM, 4D/time series, NIfTI-2, PDFs and complex/vector datatypes are not supported. PNG/JPG/WebP images and screenshots open in a separate local 2D viewer, with brightness, contrast, zoom, reset, and PNG export (up to 4096px export). Images are limited to 20 MB, 8192 pixels per side and 24 megapixels total; file signatures are checked. Single images do not create a 3D reconstruction or medical findings.

## Scope and privacy

This is a functioning visualization project, not a clinical MRI reader or a medically validated product. No AI/API analysis is implemented. It cannot detect lesions, establish an exact diagnosis, infer a cause, recommend treatment, or generate a segmented brain reconstruction. The blue reference marker is illustrative and is never attached to uploaded scans. Skull, non-brain tissue and artifacts may appear in uploaded voxel previews.

Scans are read locally in memory. No fetch or upload request contains scan data; no scan is stored in localStorage, IndexedDB, or a backend. Removing a scan clears its data and canvases. Switching to the demo retains the loaded scan until it is removed or the tab is closed. Hosting providers may still keep ordinary page-access logs. Exported PNGs contain the displayed scan and should be treated as private by the person exporting them.

## Asset credits

Human cortical PLY reference meshes: dfsp-spirit/scimesh test_data/ply/lh_mesh_sulc_viridis.ply and rh_mesh_sulc_viridis.ply, from https://github.com/dfsp-spirit/scimesh (MIT; full license in dist/assets/MESH-LICENSE.txt). Mesh positions and triangle indices were converted into little-endian binary buffers; cortical colors are generated in the app. The model represents cortical surfaces only, not the cerebellum or brainstem. Conversion format: uint32 position-float-count, uint32 index-count, float32 XYZ positions, uint32 triangle indices.

Three.js r170: MIT, dist/vendor/THREE-LICENSE.txt. Poppins: SIL Open Font License, dist/assets/POPPINS-LICENSE.txt.

## Manual verification checklist

Open the reference brain, select the example marker, expand the information, rotate, reset, toggle translucency, export PNG. Open the gzipped phantom and confirm the 3D preview changes, adjust threshold, navigate all three slice sliders, adjust contrast, switch demo/scan modes, remove the scan, and upload invalid.nii. Check narrow mobile layout and browser console errors.

## Published Alzheimer’s example
The educational example uses the unmodified Control/MCI/AD figure by Chandra, Dervenoulas & Politis / ADNI (CC BY 4.0). Attribution and source are bundled in dist/assets/ALZHEIMERS-CASE-CREDIT.txt. Uploading the exact bundled image is recognized by byte count plus SHA-256 match and reveals its existing published label, not a diagnosis inferred from pixels. Other files never inherit that label. The sample is also available through Open Alzheimer’s MRI example.
