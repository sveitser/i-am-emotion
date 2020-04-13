with import ./nix/nixpkgs.nix {
  overlays = [ (import ../overlays/python.nix) ];
};


mkShell {
  buildInputs = with python3Packages; [
       numpy
       # pytorch
       (pytorch-bin.override (old: {
         cudnn = cudnn_cudatoolkit_10;
         cudatoolkit = cudatoolkit_10;
       }))

       librosa
       
       tensorboardX
       matplotlib
       pillow
       flask
       scipy
       tqdm
       unidecode
       pysoundfile
       protobuf

       lws
       phonemizer
 
       inflect
       tensorflow
       jupyter

       black

       pydub
       scipy

       gunicorn
  ];
}
