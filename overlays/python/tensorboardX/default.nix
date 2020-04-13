{ buildPythonPackage, fetchPypi
, matplotlib
, numpy
, protobuf
, pytest
, six
, which
}:

buildPythonPackage rec {

  pname = "tensorboardX";
  version = "1.6";

  src = fetchPypi {
    inherit pname version;
    sha256 = "17gb1wcvrs87bw935j74xdjdfwmk4i2bg8h4k1qdfn24p8y2nhpi";
  };

  doCheck = false;  # doesn't find tests
  checkInputs = [ matplotlib pytest ];

  propagatedBuildInputs = [
    which
    protobuf
    numpy
    six
  ];
}
