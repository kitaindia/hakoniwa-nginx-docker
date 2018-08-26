require File.expand_path('../test_helper.rb', __FILE__)

describe 'hako-mente.cgi' do
  before(:all) do
    setup_web
  end

  after(:all){ cleanup }

  it 'has 200 status' do
    response = RestClient.get("http://localhost:5000/hako-mente.cgi")
    assert_equal 200, response.code
  end

  it 'has expected html' do
    response = RestClient.get("http://localhost:5000/hako-mente.cgi", {}).body
    expected = open(File.expand_path('../html/hako-mente.html', __FILE__)).read
    assert_equal expected, response.encode("UTF-8", "EUC-JP")
  end
end