import nock from 'nock';

beforeEach(() => {
  if (!nock.isActive()) {
    nock.activate();
  }

  nock.cleanAll();
  nock.disableNetConnect();
});

afterEach(() => {
  nock.cleanAll();
  nock.restore();
  jest.clearAllMocks();
});
