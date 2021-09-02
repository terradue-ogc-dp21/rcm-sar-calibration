# RCM harvesting, calibration and publication on S3

This repo contains a CWL document to harvest, calibrate and publish to S3 RADARSAT Constellation Mission (RCM) acquisitions.

The CWL Workflow:
- harvests the RCM metadata )
- performs the SAR calibration using SNAP
- optionaly publishes the STAC item and catalog to an S3 bucket

## Getting the RCM data

NRCAN provides access to ten RCM acquisitions in the context of the OGC Disasters Pilot 21 initiative.

Once downloaded from the FTP site, put each of the RCM zip archives in a dedicated folder as shown in the example below:

```console
$ tree RCM1_OK1721243_PK1721268_4_5M9_20200425_001248_HH_HV_GRD/
RCM1_OK1721243_PK1721268_4_5M9_20200425_001248_HH_HV_GRD/
└── RCM1_OK1721243_PK1721268_4_5M9_20200425_001248_HH_HV_GRD.zip
```

## Running the CWL Workflow

1. Get the latest CWL Workflow document release from https://github.com/terradue-ogc-dp21/rcm-sar-calibration/releases

2. Install `docker` and `cwltool`

3. Prepare a YAML parameters file with:

```yaml
rcm:
  - class: Directory
    path: RCM1_OK1721243_PK1721268_4_5M9_20200425_001248_HH_HV_GRD
sink-access-key-id: <replace with S3 access key id>
sink-secret-access-key: <replace with S3 access key>
sink-service-url: <replace with S3 service URL>
sink-region: <replace with S3 region>
sink-path: <replace with S3 path>
```

4. Run the CWL Workflow with: 

```console
cwltool rcm-calibrate.0.1.1.cwl params.yml
```
  
Done!
