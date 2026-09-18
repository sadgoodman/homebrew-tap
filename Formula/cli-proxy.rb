class CliProxy < Formula
  desc "Lightweight HTTP/HTTPS intercepting proxy with a terminal UI"
  homepage "https://github.com/sadgoodman/cli-proxy"
  license "MIT"

  on_macos do
    if Hardware::CPU.intel?
      url "https://github.com/sadgoodman/cli-proxy/releases/download/v0.1.2/cli-proxy_0.1.2_darwin_amd64.tar.gz"
      sha256 "c55721a9f8098b596d4700192f7e9f9c368c360cd2bb0d091d2f58f94514c3e3"
    end
    if Hardware::CPU.arm?
      url "https://github.com/sadgoodman/cli-proxy/releases/download/v0.1.2/cli-proxy_0.1.2_darwin_arm64.tar.gz"
      sha256 "697e108c6fb619c8c0c32209706f9f7242c6c4bdbf26891ccacc313a6d0c0141"
    end
  end

  on_linux do
    if Hardware::CPU.intel?
      url "https://github.com/sadgoodman/cli-proxy/releases/download/v0.1.2/cli-proxy_0.1.2_linux_amd64.tar.gz"
      sha256 "8f0f513023ea419ed563b5009d159b40323918e2d98646806a6214c08b18b271"
    end
    if Hardware::CPU.arm?
      url "https://github.com/sadgoodman/cli-proxy/releases/download/v0.1.2/cli-proxy_0.1.2_linux_arm64.tar.gz"
      sha256 "0593519dbc508a95f482218e849e778eeaf30a9d9ea16a2a4cc3a2729f12e934"
    end
  end

  def install
    bin.install "cli-proxy"
  end

  test do
    assert_match "cli-proxy", shell_output("#{bin}/cli-proxy -version")
  end
end
