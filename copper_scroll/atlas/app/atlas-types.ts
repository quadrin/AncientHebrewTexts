export type Candidate = { placeId: string; status: string; confidence: string };
export type Place = { id: string; name: string; shortName: string; lat: number | null; lon: number | null; precision: string; kind: string; region: string; note: string; source: string };
export type Entry = { id: string; title: string; hebrew: string; description: string; lines: string; status: string; confidence: string; region: string; candidates: Candidate[]; evidence: string; caution: string; landmark: string; period: string; sources: string; featured: boolean };
