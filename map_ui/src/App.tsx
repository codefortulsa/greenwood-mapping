import { useState, useMemo } from "react"
import { Map, Source, Layer, NavigationControl, ScaleControl } from "react-map-gl/maplibre"
import type { StyleSpecification } from "maplibre-gl"

const MARTIN_URL = import.meta.env.VITE_MARTIN_URL ?? "http://localhost:3000"

type LayerDef = {
  id: string
  table: string
  label: string
  color: string
  kind: "fill" | "line" | "outline"
  default: boolean
}

const LAYERS: LayerDef[] = [
  {
    id: "overlays_historicalshape",
    table: "overlays_historicalshape",
    label: "1921 destruction zone (curated)",
    color: "#ef4444",
    kind: "fill",
    default: true,
  },
  {
    id: "poi_footprints",
    table: "poi_footprints",
    label: "Featured POI footprints",
    color: "#f97316",
    kind: "fill",
    default: true,
  },
  {
    id: "greenwood_buildings",
    table: "greenwood_buildings",
    label: "Greenwood historic buildings",
    color: "#374151",
    kind: "fill",
    default: true,
  },
  {
    id: "greenwood_roads",
    table: "greenwood_roads",
    label: "Greenwood historic roads",
    color: "#92400e",
    kind: "line",
    default: true,
  },
  {
    id: "parcels",
    table: "parcels",
    label: "Tulsa County parcels (modern)",
    color: "#4b5563",
    kind: "outline",
    default: false,
  },
  {
    id: "quarters",
    table: "quarters",
    label: "PLSS quarter sections",
    color: "#6366f1",
    kind: "outline",
    default: false,
  },
  {
    id: "tulsa_building_footprints",
    table: "tulsa_building_footprints",
    label: "All Tulsa building footprints (modern)",
    color: "#9ca3af",
    kind: "outline",
    default: false,
  },
]

// OSM raster base. Free for demo; swap for a vector basemap later.
const baseStyle: StyleSpecification = {
  version: 8,
  sources: {
    osm: {
      type: "raster",
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxzoom: 19,
    },
  },
  layers: [
    {
      id: "osm-base",
      type: "raster",
      source: "osm",
    },
  ],
}

export default function App() {
  const [visible, setVisible] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(LAYERS.map((l) => [l.id, l.default])),
  )

  const toggle = (id: string) =>
    setVisible((v) => ({ ...v, [id]: !v[id] }))

  const sources = useMemo(() => LAYERS, [])

  return (
    <>
      <div className="legend">
        <h3>Layers</h3>
        {LAYERS.map((l) => (
          <label key={l.id}>
            <input
              type="checkbox"
              checked={visible[l.id]}
              onChange={() => toggle(l.id)}
            />
            <span className="swatch" style={{ background: l.color, opacity: l.kind === "outline" ? 0.3 : 0.55 }} />
            {l.label}
          </label>
        ))}
        <div style={{ marginTop: 6, fontSize: 11, color: "#666" }}>
          Tiles served by Martin at <code>{MARTIN_URL}</code>
        </div>
      </div>

      <Map
        initialViewState={{ longitude: -95.989, latitude: 36.16, zoom: 15 }}
        style={{ width: "100vw", height: "100vh" }}
        mapStyle={baseStyle}
      >
        <NavigationControl position="top-right" />
        <ScaleControl position="bottom-left" />

        {sources.map((l) => (
          <Source
            key={l.id}
            id={l.id}
            type="vector"
            url={`${MARTIN_URL}/${l.table}`}
          >
            {l.kind === "fill" && (
              <Layer
                id={`${l.id}-fill`}
                type="fill"
                source={l.id}
                source-layer={l.table}
                paint={{
                  "fill-color": l.color,
                  "fill-opacity": 0.45,
                  "fill-outline-color": l.color,
                }}
                layout={{ visibility: visible[l.id] ? "visible" : "none" }}
              />
            )}
            {l.kind === "line" && (
              <Layer
                id={`${l.id}-line`}
                type="line"
                source={l.id}
                source-layer={l.table}
                paint={{ "line-color": l.color, "line-width": 2 }}
                layout={{ visibility: visible[l.id] ? "visible" : "none" }}
              />
            )}
            {l.kind === "outline" && (
              <Layer
                id={`${l.id}-outline`}
                type="line"
                source={l.id}
                source-layer={l.table}
                paint={{ "line-color": l.color, "line-width": 0.5 }}
                layout={{ visibility: visible[l.id] ? "visible" : "none" }}
              />
            )}
          </Source>
        ))}
      </Map>
    </>
  )
}
