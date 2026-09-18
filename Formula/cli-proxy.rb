class CliProxy < Formula
  desc "Lightweight HTTP/HTTPS intercepting proxy with a terminal UI"
  homepage "https://github.com/sadgoodman/cli-proxy"
  license "MIT"

  on_macos do
    if Hardware::CPU.intel?
      url "https://github.com/sadgoodman/cli-proxy/releases/download/v0.1.1/cli-proxy_0.1.1_darwin_amd64.tar.gz"
      sha256 "8ce29ea0e3951417fa34d22af3162e79afad5dac7afa875c2f8b17dcc35ce500"
    end
    if Hardware::CPU.arm?
      url "https://github.com/sadgoodman/cli-proxy/releases/download/v0.1.1/cli-proxy_0.1.1_darwin_arm64.tar.gz"
      sha256 "b9bb49ad501da311ba4dd0e2320c18872c7d22f127f87fa8c45dd8b2c271c026"
    end
  end

  on_linux do
    if Hardware::CPU.intel?
      url "https://github.com/sadgoodman/cli-proxy/releases/download/v0.1.1/cli-proxy_0.1.1_linux_amd64.tar.gz"
      sha256 "bdbe91544b54ad9ae10c92cc544f3d7306606fc06ab8a11edaf2487f052dcfa0"
    end
    if Hardware::CPU.arm?
      url "https://github.com/sadgoodman/cli-proxy/releases/download/v0.1.1/cli-proxy_0.1.1_linux_arm64.tar.gz"
      sha256 "3f0aba8b8b89986df4ce1e5ba86af20b669ab5623b09fa95b02823d54ea99062"
    end
  end

  def install
    bin.install "cli-proxy"
  end

  test do
    assert_match "cli-proxy", shell_output("#{bin}/cli-proxy -version")
  end
end
