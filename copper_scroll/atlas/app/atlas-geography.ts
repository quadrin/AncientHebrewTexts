import type { Entry, Place } from "./atlas-types";

export function precisionRadius(place: Place) {
  const match = place.precision.match(/([\d.]+)\s*(km|m)/);
  return match ? Number(match[1]) * (match[2] === "km" ? 1000 : 1) : 400;
}
export function candidateBounds(place: Place): [[number, number], [number, number]] | null {
  if (place.lat === null || place.lon === null) return null;
  const radius = precisionRadius(place);
  const dy = radius / 111320, dx = dy / Math.cos(place.lat * Math.PI / 180);
  return [[place.lon - dx, place.lat - dy], [place.lon + dx, place.lat + dy]];
}
// The gazetteer supplies anchors and precision estimates, not surveyed site outlines.
export function candidateAreas(entry: Entry, places: Place[], focusId: string | null) {
  return { type: "FeatureCollection" as const, features: entry.candidates.flatMap(candidate => {
    const p = places.find(place => place.id === candidate.placeId);
    if (!p || p.lat === null || p.lon === null) return [];
    const radius = precisionRadius(p), lat = p.lat, lon = p.lon;
    const ring = Array.from({length: 65}, (_, i) => {
      const angle = i / 64 * Math.PI * 2;
      return [lon + Math.cos(angle) * radius / (111320 * Math.cos(lat * Math.PI / 180)), lat + Math.sin(angle) * radius / 111320];
    });
    ring[64] = [...ring[0]];
    return [{type: "Feature" as const, properties: {placeId: p.id, selected: p.id === focusId, status: candidate.status}, geometry: {type: "Polygon" as const, coordinates: [ring]}}];
  }) };
}
