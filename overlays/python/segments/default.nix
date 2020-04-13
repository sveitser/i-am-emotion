{ buildPythonPackage
, fetchPypi
, six
, clldutils
, regex
}:

buildPythonPackage rec {

  pname = "segments";
  version = "2.0.1";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0apvsvw1rdrwrrmz03r7d44ljns3mhn4ggf5x7k9v6xyz4311wg9";
  };

  propagatedBuildInputs = [
    clldutils
    six
    regex
  ];
}
