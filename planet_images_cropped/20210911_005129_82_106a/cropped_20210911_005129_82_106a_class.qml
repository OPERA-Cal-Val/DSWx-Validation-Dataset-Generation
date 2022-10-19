<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.24.2-Tisler" maxScale="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal fetchMode="0" mode="0" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option type="QString" value="Value" name="identify/format"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" value="" name="name"/>
      <Option name="properties"/>
      <Option type="QString" value="collection" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" enabled="false" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer type="paletted" nodataColor="" band="1" opacity="1" alphaBand="-1">
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <colorPalette>
        <paletteEntry alpha="255" label="0 - Unclassified" value="0" color="#000000"/>
        <paletteEntry alpha="255" label="1 - Water Dark" value="1" color="#c38302"/>
        <paletteEntry alpha="255" label="2 - Water green" value="2" color="#33982e"/>
        <paletteEntry alpha="255" label="3 - Water bright" value="3" color="#cb914f"/>
        <paletteEntry alpha="255" label="4 - Veg" value="4" color="#dcece7"/>
        <paletteEntry alpha="255" label="5 - Veg 2" value="5" color="#6787df"/>
        <paletteEntry alpha="255" label="6 - purple" value="6" color="#ee488c"/>
        <paletteEntry alpha="255" label="7 - road" value="7" color="#cf8b7c"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
    <huesaturation invertColors="0" colorizeBlue="128" grayscaleMode="0" colorizeRed="255" colorizeStrength="100" saturation="0" colorizeOn="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
