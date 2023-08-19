{
  description = "test shell";

  outputs = { self, nixpkgs }: let
    pkgs = import nixpkgs {
      system = "x86_64-linux";
    };
  in {
    devShells.x86_64-linux.default = with pkgs; 
      let
        my-python-packages = p: with p; [
          numpy
          matplotlib
          # other python packages
        ];
        my-python = pkgs.python3.withPackages my-python-packages;
      in my-python.env
    ;
  };
}
