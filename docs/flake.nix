{
  description = "Docusaurus documentation development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            # Node.js 20 LTS for Docusaurus 3.x compatibility
            nodejs_20
            # Include npm and npx
            nodePackages.npm
            # Useful for debugging and file watching
            nodePackages.nodemon
            # For serving built docs locally
            nodePackages.serve
          ];

          shellHook = ''
            echo "📚 Docusaurus development environment"
            echo "Node.js version: $(node --version)"
            echo "npm version: $(npm --version)"
            echo ""
            echo "Available commands:"
            echo "  npm install       - Install dependencies"
            echo "  npm start         - Start dev server (port 3000)"
            echo "  npm run build     - Build static site"
            echo "  npm run serve     - Serve built site (port 3000)"
            echo ""
          '';
        };
      }
    );
}
