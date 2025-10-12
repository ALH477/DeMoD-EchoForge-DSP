{
  description = "Flake to process the DSP audio interface schematic script";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    overlays = [
      (final: prev: rec {
        python3 = prev.python3.override {
          packageOverrides = pself: psuper: {
          simp-sexp = pself.buildPythonPackage rec {
            pname = "simp-sexp";
            version = "0.3.0";
            format = "pyproject";
            src = pself.fetchPypi {
              inherit pname;
              inherit version;
              hash = "sha256-nQxXvV+EALn+VY6ja3UYBn3b5yehBrFJjH+hBLd8HKE=";
            };
            nativeBuildInputs = with pself; [ setuptools ];
          };

          inspice = pself.buildPythonPackage rec {
            pname = "InSpice";
            version = "1.6.4.1";
            format = "pyproject";
            src = pself.fetchPypi {
              inherit pname;
              inherit version;
              hash = "sha256-gLcUQnbWSRdWGNMHbC3MuCus+p1AYGjU25IY5murMzM=";
            };
            nativeBuildInputs = with pself; [ setuptools ];
          };

          kinet2pcb = pself.buildPythonPackage rec {
            pname = "kinet2pcb";
            version = "1.1.2";
            format = "pyproject";
            src = pself.fetchPypi {
              inherit pname;
              inherit version;
              hash = "sha256-fqJxOiXLJTXPJxT92tR7apWSjO+RaEBW9LJ3n9EOwZM=";
            };
            nativeBuildInputs = with pself; [ setuptools ];
            propagatedBuildInputs = with pself; [ pyparsing ];
          };

          skidl = pself.buildPythonPackage rec {
            pname = "skidl";
            version = "2.1.1";
            format = "pyproject";
            src = pself.fetchPypi {
              inherit pname;
              inherit version;
              hash = "sha256-8SdUSqH4Z1yiYsg4Ros/oCAH3hr2oueZZFDnJ4wo0oU=";
            };
            nativeBuildInputs = with pself; [ setuptools ];
            propagatedBuildInputs = with pself; [ kinet2pcb simp-sexp inspice ply graphviz deprecation ];
          };
        };
        };
      })
    ];
    pkgs = import nixpkgs { inherit system; inherit overlays; };
    myPython = pkgs.python3.withPackages (ps: with ps; [
      skidl
      kinet2pcb
      pyparsing
      ply
      graphviz
      deprecation
      simp-sexp
      inspice
    ]);
  in {
    packages.${system}.default = pkgs.stdenv.mkDerivation {
      name = "dsp-schematic";
      src = self;

      buildInputs = [ myPython pkgs.kicad-small pkgs.ngspice ];

      buildPhase = ''
        cp $src/pasted-text.txt schematic.py
        sed -i "s|'/usr/share/kicad/library'|'${pkgs.kicad-small}/share/kicad/library'|g" schematic.py
        python schematic.py
      '';

      installPhase = ''
        mkdir -p $out
        cp production_dsp_schematic.kicad_sch $out/
      '';
    };

    devShells.${system}.default = pkgs.mkShell {
      packages = [ myPython pkgs.kicad-small pkgs.ngspice ];
      shellHook = ''
        export PYTHONPATH="$PYTHONPATH:${pkgs.kicad-small}/share/kicad/scripting"
        export KICAD_LIBRARY_PATH="${pkgs.kicad-small}/share/kicad/library"
        echo "Run python schematic.py to generate the schematic"
      '';
    };
  };
}
