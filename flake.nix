{
  description = "template";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        # ENVIRONMENT_VARIABLE = "SOMTHING";

        packages = with pkgs; [
          (python314.withPackages (
            ps: with ps; [
              scikit-learn
              seaborn
              numpy
              pandas
              matplotlib
              ipython
            ]
          ))
          mpremote
          uv
        ];

        shellHook = ''
          exec nu
        '';
      };
    };
}
