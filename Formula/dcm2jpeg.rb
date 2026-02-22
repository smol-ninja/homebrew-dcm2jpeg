class Dcm2jpeg < Formula
  include Language::Python::Virtualenv

  desc "Convert DICOM files to JPEG"
  homepage "https://github.com/smol-ninja/homebrew-dcm2jpeg"
  url "https://github.com/smol-ninja/homebrew-dcm2jpeg/archive/refs/tags/v1.1.0.tar.gz"
  sha256 "b8c9022811c8f6f6d4ea0f2a459861db5b2e5769715f45893dc3fff755a6b0df"
  license "MIT"

  depends_on "numpy"
  depends_on "pillow"
  depends_on "python@3.13"

  resource "pydicom" do
    url "https://files.pythonhosted.org/packages/d7/6f/55ea163b344c91df2e03c007bebf94781f0817656e2c037d7c5bf86c3bfc/pydicom-3.0.1.tar.gz"
    sha256 "7b8be344b5b62493c9452ba6f5a299f78f8a6ab79786c729b0613698209603ec"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "Convert DICOM", shell_output("#{bin}/dcm2jpeg --help")
  end
end
