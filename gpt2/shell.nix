with import ./nix/nixpkgs.nix {};

mkShell {

  SOURCE_DATE_EPOCH="315532800";

  buildInputs = [
    google-cloud-sdk
    (python3.buildEnv.override {
      extraLibs = with python3Packages; [
        (fire.overridePythonAttrs (old: {
         doCheck = false;
        }))
        (tensorflowWithCuda.override { 
          cudnn = cudnn_cudatoolkit_10;
          cudatoolkit = cudatoolkit_10;
        })
        regex
        ipython
        python-language-server
        flask
        black
        spacy
        spacy_models.en_core_web_sm
        unidecode
        gunicorn
      ];
      ignoreCollisions = true;
    })
  ];
  shellHook = ''
    export PYTHONPATH=src
  '';

}

# with python36Packages;

# buildPythonPackage {
#   pname = "gpt2";
#   version = "0.1";

#   src = ./.;

#   propagatedBuildInputs = [
#     fire
#     tensorflowWithCuda
#     regex
#     ipython
#     python-language-server
#   ];
# }
