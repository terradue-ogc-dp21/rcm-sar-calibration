from snapista import Graph
from snapista import Operator
from lxml import etree
import numpy as np

def get_mode(item):

    tree = etree.parse(item.get_assets()["metadata"].get_absolute_href())
    #return tree.xpath("/product/sourceAttributes/beamMode")[0].text
    return tree.xpath("(//*[local-name()='beamMode'])")[0].text
    #return tree.getroot()[5][5].text

def get_target_resolution(mode):

    resolution = {}
    resolution["Low Resolution 100m"] = 100
    resolution["Medium Resolution 50m"] = 50
    resolution["Medium Resolution 30m"] = 30
    resolution["Medium Resolution 16m"] = 16
    resolution["High Resolution 5m"] = 5
    resolution["Very High Resolution 3m"] = 3
    resolution["Low Noise"] = 100
    # Spotlight = 1 x 3 ??? TBD
    resolution["Spotlight"] = 1#3
    resolution["Quad-Polarization"] = 9

    return resolution[mode]


def get_nlooks(item,res):

    sp_range = float(item.properties["sar:pixel_spacing_range"])
    sp_az = float(item.properties["sar:pixel_spacing_azimuth"])

    return int(np.round(np.sqrt(res * res)/(sp_range * sp_az)))

def read_ml(item):


    g = Graph()

    mode = get_mode(item)
    target_res = get_target_resolution(mode)
    nlooks = get_nlooks(item,target_res)

    file_path_safe = item.get_assets()["manifest"].get_absolute_href().replace("file://", "")

    g.add_node(
            operator=Operator(
                "Read",
                file="$manifest",
            ),
            node_id="read",
    )

    g.add_node(
    operator=Operator("Calibration", outputSigmaBand="true"),
    node_id="calibration",
    source="read",
    )

    g.add_node(
        operator=Operator(
            "Multilook",
            nRgLooks=f"{nlooks}",
            nAzLooks=f"{nlooks}",
            outputIntensity="true",
            grSquarePixel="true"
            ),
        node_id="multilook",
        source="calibration",
    )

    g.add_node(
            operator=Operator("Write", file="$multilook", formatName="BEAM-DIMAP"),
            node_id="write",
            source="multilook",
    )

    g.save_graph("graph1.xml")

def ml_db(item):

    mode = get_mode(item)
    target_res = get_target_resolution(mode)

    g = Graph()

    g.add_node(
            operator=Operator(
                "Read",
                file="$multilook",
            ),
            node_id="read",
        )


    g.add_node(
        operator=Operator(
            "Terrain-Correction",
            pixelSpacingInMeter=f"{target_res}",
            demName="SRTM 1Sec HGT",
            mapProjection="AUTO:42001",
        ),
        node_id="terrain-correction",
        source="read",
    )

    g.add_node(
        operator=Operator("LinearToFromdB"),
        node_id="linear",
        source="terrain-correction",
    )

    g.add_node(
        operator=Operator("Write", file="$calibrated", formatName="GeoTIFF-BigTIFF"),
        node_id="write",
        source="linear",
    )

    g.save_graph("graph2.xml")

def ml_sf(item):

    mode = get_mode(item)
    target_res = get_target_resolution(mode)

    g = Graph()

    g.add_node(
            operator=Operator(
                "Read",
                file="$multilook",
            ),
            node_id="read",
        )

    g.add_node(
            operator=Operator(
                "Speckle-Filter",
                filter="Lee Sigma",
                filterSizeX="3",
                filterSizeY="3",
                dampingFactor="2",
                estimateENL="true",
                enl="1.0",
                numLooksStr="1",
                windowSize="7x7",
                targetWindowSizeStr="3x3",
                sigmaStr="0.9",
                anSize="50",
            ),
            node_id="speckle-filter",
            source="read",
    )

    g.add_node(
        operator=Operator(
            "Terrain-Correction",
            pixelSpacingInMeter=f"{target_res}",
            demName="SRTM 1Sec HGT",
            mapProjection="AUTO:42001"
        ),
        node_id="terrain-correction",
        source="speckle-filter",
    )

    g.add_node(
        operator=Operator("LinearToFromdB"),
        node_id="linear",
        source="terrain-correction",
    )

    g.add_node(
        operator=Operator("Write", file="$overview", formatName="GeoTIFF-BigTIFF"),
        node_id="write",
        source="linear",
    )

    g.save_graph("graph3.xml")