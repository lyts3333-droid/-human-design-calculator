export type PlanetInfo = {
  planet: string;
  gate: number;
  line: number;
  gate_line: string;
  sign?: string;
  longitude?: number;
  constellation_symbol?: string;
  arrow_direction?: string;
};

export type HumanDesignResult = {
  input_date?: string;
  profile?: string;
  type?: string;
  type_name?: string;
  strategy?: string;
  decision_mode?: string;
  authority?: string;
  not_self_theme?: string;
  personality_list?: PlanetInfo[];
  design_list?: PlanetInfo[];
};

export type CalculateResponse = {
  status: "success" | "error";
  data?: HumanDesignResult;
  error?: string;
};

export type GeneKeyDetail = {
  name: string;
  meaning?: string;
  shadow?: string;
  manifestation?: string;
  gift?: string;
  transformation?: string;
  siddhi?: string;
  finalState?: string;
  synthesis?: string;
  error?: string;
};

export type BirthFormValues = {
  name: string;
  year: number;
  month: number;
  day: number;
  time: string;
  region: "taiwan" | "china" | "";
  county: string;
  district: string;
  timezone: string;
  longitude: number;
  latitude: number;
};
