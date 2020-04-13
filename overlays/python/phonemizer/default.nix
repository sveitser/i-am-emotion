{ buildPythonPackage
, fetchFromGitHub
, numpy
, scipy
, segments
, joblib
, espeak
}:

buildPythonPackage rec {

  pname = "phonemizer";
  version = "1.0";

  src = fetchFromGitHub {
    owner = "bootphon";
    repo = "phonemizer";
    rev = "f470ffb4af63d079c373a1beb5d76f24bc5752b0";
    sha256 = "07z48bvlpimmh9383mfqhnxygmkx686w9b864zhvnyia4yiphydp";
  };

  propagatedBuildInputs = [
    espeak
    segments
    joblib
  ];
}
