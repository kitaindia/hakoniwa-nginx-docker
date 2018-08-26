require 'minitest/autorun'
require 'minitest/hooks/default'
require 'rest-client'

class MiniTest::Test

  def setup_web
    system "docker build -t hakoniwa ."
    system "docker run  -d -p 5000:80 --name='hakoniwa-test' hakoniwa >/dev/null 2>&1"
    begin
      RestClient.get("http://localhost:5000/hako-main.cgi")
    rescue
      sleep 1
      retry
    end
  end

  def cleanup
    system "docker rm -f hakoniwa-test >/dev/null 2>&1"
  end
end
