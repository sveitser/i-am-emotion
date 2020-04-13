{ buildPythonPackage, fetchPypi
, numpy
, scipy
}:

buildPythonPackage rec {

  pname = "bandmat";
  version = "0.7";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0nzhy4vf4jcd14v5jddz877yvaqv8n2pajwshgnh92jds3c45apr";
  };

  propagatedBuildInputs = [
    numpy
    scipy
  ];
}
