{ buildPythonPackage, fetchPypi
, git
, bandmat
, coverage
, cython
, fastdtw
, nose
, numpy
, pysptk
, scikitlearn
, tqdm
}:

buildPythonPackage rec {

  pname = "nnmnkwii";
  version = "0.0.17";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0jg5gk1cb90hhpdar8y72rdgqsb8lis78j1rfmibq6k3mw8d0jr2";
  };
  # src = fetchFromGitHub {
  #   inherit pname
  #   owner = "r9y9";
  #   rev = "$version";
  #   sha256 = "1yjhvakz0ai65i7n4ah5kakfgpp1inz9fghdvchhhl1a1s2scqfp";
  # };

  patchPhase = ''
    sed -i 's|sklearn|scikit-learn|g' setup.py
  '';

  doCheck = false;
  checkInputs = [ coverage nose ];
  nativeBuildInputs = [ git ];
  buildInputs = [ cython ];

  propagatedBuildInputs = [
    git
    bandmat
    fastdtw
    pysptk
    numpy
    scikitlearn
    tqdm
  ];
}
