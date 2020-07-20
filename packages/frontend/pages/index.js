import Layout from '../components/Layout';
import LiveNow from '../components/LiveNow';

import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'

process.on('unhandledRejection', (reason, p) => {
  console.log('Unhandled Rejection at: Promise', p, 'reason:', reason);
  // application specific logging, throwing an error, or other logic here
});

const BetaDisclaimer = () => (
      <Container>
      <Row className="beta-disclaimer">
      <Col md="auto">
             <svg id="beta-disclaimer-icon" xmlns="http://www.w3.org/2000/svg" height="100" viewBox="0 0 24 24" preserveAspectRatio="xMaxYMax meet" width="100">
                <path d="M0 0h24v24H0z" fill="none"/>
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
      </Col>
      <Col className="beta-text">
              <h1>Velkommen til nye frikanalen.no!</h1>
              <p>Etter mye hardt arbeide bak scenene kan vi endelig presentere
              første versjon av nye frikanalen.no.</p>
              <p> Det er i første omgang nødvendig å bruke <a
                href="https://forrige.frikanalen.no/">de gamle nettsidene</a> for å laste opp
                innhold, eller se i videoarkivet.</p>
              <p>De eksisterende funksjonene vil bli implementert fortløpende
              på den nye siden!</p>
      </Col>
      </Row>
      <style jsx global>{`
        .beta-disclaimer {
            background-color: black;
            opacity: .6;
            color: white;
            margin-bottom: 20px;
        }
        #beta-disclaimer-icon {
            fill: yellow;
            margin: 30px auto;
        }
        .beta-text {
            padding-left: 0px;
            padding-right: 20px;
            font-family: 'Roboto', sans-serif;
            }

        a {
            color: #aaaaff;
            text-decoration: underline;
        }
      `}</style>
      </Container>
)

export default function index() {
  return (
    <Layout>
      <BetaDisclaimer/>
      <LiveNow/>
      <style jsx global>{`
      main {
        padding-top: 20px;
      }
      `}</style>
    </Layout>
  );
}
