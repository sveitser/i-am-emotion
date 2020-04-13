{ buildPythonPackage, fetchPypi
, git
, coverage
, decorator
, nose
, numpy
, six
}:

buildPythonPackage rec {

  pname = "pysptk";
  version = "0.1.9";

  src = fetchPypi {
    inherit pname version;
    sha256 = "15bncaixrjkhnhsjvi38zyphrw0wdgg1qr0crpczxxml2m5gn5hx";
  };

  checkInputs = [ coverage nose ];
  nativeBuildInputs = [ git ];

  propagatedBuildInputs = [
    git
    decorator
    numpy
    six
  ];
}
