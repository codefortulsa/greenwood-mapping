import { useState } from "react"
import { Map, Source, Layer, NavigationControl, ScaleControl } from "react-map-gl/maplibre"
import type { StyleSpecification, FilterSpecification } from "maplibre-gl"

const MARTIN_URL = import.meta.env.VITE_MARTIN_URL ?? "http://localhost:3000"

// Single Martin source. Each on-screen layer filters by MapFeature.kind.
const FEATURE_SOURCE = "overlays_mapfeature"

type LayerDef = {
  id: string
  kind: string
  label: string
  color: string
  render: "fill" | "line" | "outline"
  default: boolean
}

const LAYERS: LayerDef[] = [
  { id: "destruction_zone",          kind: "destruction_zone",          label: "1921 destruction zone",      color: "#ef4444", render: "fill",    default: true },
  { id: "poi_footprint",             kind: "poi_footprint",             label: "Featured POI footprints",    color: "#f97316", render: "fill",    default: true },
  { id: "historical_building",       kind: "historical_building",       label: "Historical buildings",       color: "#374151", render: "fill",    default: true },
  { id: "historical_road",           kind: "historical_road",           label: "Historical roads",           color: "#92400e", render: "line",    default: true },
  { id: "parcel",                    kind: "parcel",                    label: "Parcels (modern)",           color: "#4b5563", render: "outline", default: false },
  { id: "quarter_section",           kind: "quarter_section",           label: "PLSS quarter sections",      color: "#6366f1", render: "outline", default: false },
  { id: "township",                  kind: "township",                  label: "PLSS townships",             color: "#8b5cf6", render: "outline", default: false },
  { id: "modern_building_footprint", kind: "modern_building_footprint", label: "Modern building footprints", color: "#9ca3af", render: "outline", default: false },
]

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
    { id: "osm-base", type: "raster", source: "osm" },
  ],
}

const kindFilter = (kind: string): FilterSpecification =>
  ["==", ["get", "kind"], kind]

export default function App() {
  const [visible, setVisible] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(LAYERS.map((l) => [l.id, l.default])),
  )

  const toggle = (id: string) => setVisible((v) => ({ ...v, [id]: !v[id] }))

  return (
    <>
      <div className="legend">
        <h3>Layers</h3>
        {LAYERS.map((l) => (
          <label key={l.id}>
            <input type="checkbox" checked={visible[l.id]} onChange={() => toggle(l.id)} />
            <span
              className="swatch"
              style={{ background: l.color, opacity: l.render === "outline" ? 0.3 : 0.55 }}
            />
            {l.label}
          </label>
        ))}
        <div style={{ marginTop: 6, fontSize: 11, color: "#666" }}>
          Martin: <code>{MARTIN_URL}/{FEATURE_SOURCE}</code>
        </div>
      </div>

      <Map
        initialViewState={{ longitude: -95.989, latitude: 36.16, zoom: 15 }}
        style={{ width: "100vw", height: "100vh" }}
        mapStyle={baseStyle}
      >
        <NavigationControl position="top-right" />
        <ScaleControl position="bottom-left" />

        <Source id={FEATURE_SOURCE} type="vector" url={`${MARTIN_URL}/${FEATURE_SOURCE}`}>
          {LAYERS.map((l) => {
            const filter = kindFilter(l.kind)
            const visibility = visible[l.id] ? "visible" : "none"
            if (l.render === "fill") {
              return (
                <Layer
                  key={l.id}
                  id={l.id}
                  type="fill"
                  source={FEATURE_SOURCE}
                  source-layer={FEATURE_SOURCE}
                  filter={filter}
                  paint={{
                    "fill-color": l.color,
                    "fill-opacity": 0.45,
                    "fill-outline-color": l.color,
                  }}
                  layout={{ visibility }}
                />
              )
            }
            if (l.render === "line") {
              return (
                <Layer
                  key={l.id}
                  id={l.id}
                  type="line"
                  source={FEATURE_SOURCE}
                  source-layer={FEATURE_SOURCE}
                  filter={filter}
                  paint={{ "line-color": l.color, "line-width": 2 }}
                  layout={{ visibility }}
                />
              )
            }
            return (
              <Layer
                key={l.id}
                id={l.id}
                type="line"
                source={FEATURE_SOURCE}
                source-layer={FEATURE_SOURCE}
                filter={filter}
                paint={{ "line-color": l.color, "line-width": 0.5 }}
                layout={{ visibility }}
              />
            )
          })}
        </Source>
      </Map>
    </>
  )
}
