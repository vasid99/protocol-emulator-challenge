{
  lib,
  fetchFromGitHub,
  rustPlatform,
}:

rustPlatform.buildRustPackage (finalAttrs: {
  pname = "customasm";
  version = "0.14.2";

  src = fetchFromGitHub {
    owner = "hlorenzi";
    repo = "customasm";
    tag = "v${finalAttrs.version}";
    hash = "sha256-Ocxi8UyDU+ASME/ZjgeuAXBIpq1kutH+IOjA1VJnA9w=";
  };

  cargoHash = "sha256-viqjNQhzXnOTTENeGcAJW5pJyMXF9qJsMm/4Xri/2mo=";

  meta = {
    description = "An assembler for custom, user-defined instruction sets";
    homepage = "https://github.com/hlorenzi/customasm";
    license = lib.licenses.asl20;
    maintainers = [ ];
  };
})
