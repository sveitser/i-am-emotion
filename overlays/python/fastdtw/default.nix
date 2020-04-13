{ buildPythonPackage, fetchPypi
, numpy
, pytest
, pytestrunner
}:

buildPythonPackage rec {

  pname = "fastdtw";
  version = "0.3.2";

  src = fetchPypi {
    inherit pname version;
    sha256 = "1yfz0nvwa5z7wny9lgjh7ysrk14d9fpgybb90dyghwpbm1i4v8h9";
  };

  doCheck = false;  # finds no tests
  checkInputs = [ pytest pytestrunner ];

  propagatedBuildInputs = [
    numpy numpy.blas
    pytest pytestrunner # shouldn't be needed, but is
  ];
}
