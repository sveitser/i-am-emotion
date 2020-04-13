{ buildPythonPackage
, fetchPypi
, openmpi
, tensorflow
}:

buildPythonPackage rec {

  pname = "horovod";
  version = "0.9.9";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0gmsgkfalm4pd2xyq5k6cpfk00xw0z6198rih7qdps3zx26djhwy";
  };

  nativeBuildInputs = [
    openmpi
  ];

  propagatedBuildInputs = [
    tensorflow
  ];

  doCheck = false;
}
