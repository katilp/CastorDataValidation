// -*- C++ -*-
//
// Package:    DemoAnalyzer
// Class:      DemoAnalyzer
// 
/**\class DemoAnalyzer DemoAnalyzer.cc Demo/DemoAnalyzer/src/DemoAnalyzer.cc

 Description: [one line class summary]

 Implementation:
 [Notes on implementation]
 */
//
// Original Author:  
//         Created:  Mon May  4 15:24:13 CEST 2015
//         Finalized: February 24, 2016  by   A. Geiser
//                    with contributions from I. Dutta, 
//                                            H. Hirvonsalo
//                                            B. Sheeran
//                                            H. Van Haevermaet
// $Id$
// ..
//
// ***************************************************************************
// version of DEMO setup provided by CMS open data access team               *
// expanded/upgraded to contain basic analysis examples for CASTOR objects   *
// ***************************************************************************

// system include files
#include <memory>

// user include files, general
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

//------ EXTRA HEADER FILES--------------------//
#include "math.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/Ref.h"

// for Root histogramming
#include "TH1.h"
#include "TH2.h"
#include "TMath.h"

//-- Vertex
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

// HF Calotower
#include "DataFormats/CaloTowers/interface/CaloTower.h"
#include "DataFormats/CaloTowers/interface/CaloTowerFwd.h"
#include "DataFormats/CaloTowers/interface/CaloTowerDetId.h"

#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/HcalDetId/interface/HcalSubdetector.h"

// for CASTOR information
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/HcalRecHit/interface/CastorRecHit.h"

#include "DataFormats/CastorReco/interface/CastorTower.h"

#include "DataFormats/JetReco/interface/BasicJet.h"
#include "DataFormats/JetReco/interface/CastorJetID.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/Luminosity/interface/LumiDetails.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "DataFormats/Scalers/interface/LumiScalers.h"


// class declaration
//

class DemoAnalyzer: public edm::EDAnalyzer {
public:
	explicit DemoAnalyzer(const edm::ParameterSet&);
	~DemoAnalyzer();

private:
	virtual void beginJob();
	virtual void analyze(const edm::Event&, const edm::EventSetup&);
	virtual void endJob();
	bool providesGoodLumisection(const edm::Event& iEvent);

	// ----------member data ---------------------------

// declare Root histograms
// for a description of their content see below

  TH1D *hRecHit_energy, *hRecHit_module, *hRecHit_sector, *hRecHit_5Msector, *hRecHit_channel;
  TH2D *hRecHit_map, *hRecHit_occupancy;

  TH1D *hTower_energy, *hLTower_energy, *hTower_multi, *hTower_phi, *hTower_eem, *hTower_ehad, *hTower_fem, *hTower_depth, *hTower_fhot, *hTower_ncell;

  TH1D *hJet_energy, *hJet_phi, *hJet_eem, *hJet_ehad, *hJet_fem, *hJet_depth, *hJet_fhot, *hJet_ntower, *hJet_sigmaz, *hJet_width;
  TH1D *hHADJet_energy, *hHADJet_calenergy, *hJet_calenergy, *hEMJet_energy;

  TH1D *hCASTOR_totalE_towers, *hCASTOR_totalE_80rechits, *hCASTOR_totalE_allrechits;

  TH1D *hNPV;
  TH1D *hEventSelection;
  int Nevents;

  double myPI;

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//

DemoAnalyzer::DemoAnalyzer(const edm::ParameterSet& iConfig) {

//now do what ever initialization is needed
edm::Service<TFileService> fs;

// ************************************
// book histograms and set axis labels
// (called once for initialization)
// ************************************

TH1::SetDefaultSumw2();

// rechits
hRecHit_energy = fs->make<TH1D>("hRecHit_energy", "hRecHit_energy", 100, 0., 100.); 
hRecHit_energy->GetXaxis()->SetTitle("RecHit E (in GeV)");
hRecHit_energy->GetYaxis()->SetTitle("Number of Events");

hRecHit_module = fs->make<TH1D>("hRecHit_module", "hRecHit_module", 14, 1, 15); 
hRecHit_module->GetXaxis()->SetTitle("module");
hRecHit_module->GetYaxis()->SetTitle("Mean energy");

hRecHit_sector = fs->make<TH1D>("hRecHit_sector", "hRecHit_sector", 16, 1, 17); 
hRecHit_sector->GetXaxis()->SetTitle("sector");
hRecHit_sector->GetYaxis()->SetTitle("Mean energy");

hRecHit_5Msector = fs->make<TH1D>("hRecHit_5Msector", "hRecHit_5Msector", 16, 1, 17); 
hRecHit_5Msector->GetXaxis()->SetTitle("sector (5 modules)");
hRecHit_5Msector->GetYaxis()->SetTitle("Mean energy");

hRecHit_channel = fs->make<TH1D>("hRecHit_channel", "hRecHit_channel", 224, 1, 225); 
hRecHit_channel->GetXaxis()->SetTitle("channel");
hRecHit_channel->GetYaxis()->SetTitle("Mean energy");

hRecHit_map = fs->make<TH2D>("hRecHit_map", "hRecHit_map", 16, 1, 17, 14, 1, 15); 
hRecHit_map->GetXaxis()->SetTitle("sector");
hRecHit_map->GetYaxis()->SetTitle("module");

hRecHit_occupancy = fs->make<TH2D>("hRecHit_occupancy", "hRecHit_occupancy", 16, 1, 17, 14, 1, 15); 
hRecHit_occupancy->GetXaxis()->SetTitle("sector");
hRecHit_occupancy->GetYaxis()->SetTitle("module");

// towers
hTower_energy = fs->make<TH1D>("hTower_energy", "hTower_energy", 100, 0., 500.); 
hTower_energy->GetXaxis()->SetTitle("Tower E (in GeV)");
hTower_energy->GetYaxis()->SetTitle("Number of Events");

hLTower_energy = fs->make<TH1D>("hLTower_energy", "hLTower_energy", 100, 0., 500.); 
hLTower_energy->GetXaxis()->SetTitle("Leading tower E (in GeV)");
hLTower_energy->GetYaxis()->SetTitle("Number of Events");

hTower_multi = fs->make<TH1D>("hTower_multi", "hTower_multi", 17, 0, 17); 
hTower_multi->GetXaxis()->SetTitle("Tower multiplicity");
hTower_multi->GetYaxis()->SetTitle("Number of Events");

hTower_phi = fs->make<TH1D>("hTower_phi", "hTower_phi", 16, -3.1416, 3.1416); 
hTower_phi->GetXaxis()->SetTitle("Tower phi");
hTower_phi->GetYaxis()->SetTitle("Number of Events");

hTower_fem = fs->make<TH1D>("hTower_fem", "hTower_fem", 50, -1, 2); 
hTower_fem->GetXaxis()->SetTitle("Tower fem");
hTower_fem->GetYaxis()->SetTitle("Number of Events");

hTower_eem = fs->make<TH1D>("hTower_eem", "hTower_eem", 100, 0., 500.); 
hTower_eem->GetXaxis()->SetTitle("Tower EM E (in GeV)");
hTower_eem->GetYaxis()->SetTitle("Number of Events");

hTower_ehad = fs->make<TH1D>("hTower_ehad", "hTower_ehad", 100, 0., 500.); 
hTower_ehad->GetXaxis()->SetTitle("Tower HAD E (in GeV)");
hTower_ehad->GetYaxis()->SetTitle("Number of Events");

hTower_fhot = fs->make<TH1D>("hTower_fhot", "hTower_fhot", 50, -1, 2); 
hTower_fhot->GetXaxis()->SetTitle("Tower fhot");
hTower_fhot->GetYaxis()->SetTitle("Number of Events");

hTower_depth = fs->make<TH1D>("hTower_depth", "hTower_depth", 100, -16000, -14000); 
hTower_depth->GetXaxis()->SetTitle("Tower depth");
hTower_depth->GetYaxis()->SetTitle("Number of Events");

hTower_ncell = fs->make<TH1D>("hTower_ncell", "hTower_ncell", 14, 1, 15); 
hTower_ncell->GetXaxis()->SetTitle("Tower ncell");
hTower_ncell->GetYaxis()->SetTitle("Number of Events");

// jets
double_t jetbins[12] = {150, 190, 230, 290, 360, 455, 575, 710, 890, 1120, 1400, 1750};
hJet_energy = fs->make<TH1D>("hJet_energy", "hJet_energy", 11, jetbins); 
hJet_energy->GetXaxis()->SetTitle("Jet E [GeV]");
hJet_energy->GetYaxis()->SetTitle("Number of Events");

hJet_calenergy = fs->make<TH1D>("hJet_calenergy", "hJet_calenergy", 11, jetbins); 
hJet_calenergy->GetXaxis()->SetTitle("Calibrated Jet E [GeV]");
hJet_calenergy->GetYaxis()->SetTitle("Number of Events");

hJet_phi = fs->make<TH1D>("hJet_phi", "hJet_phi", 16, -3.1416, 3.1416); 
hJet_phi->GetXaxis()->SetTitle("Jet phi");
hJet_phi->GetYaxis()->SetTitle("Number of Events");

hJet_fem = fs->make<TH1D>("hJet_fem", "hJet_fem", 50, -1, 2); 
hJet_fem->GetXaxis()->SetTitle("Jet fem");
hJet_fem->GetYaxis()->SetTitle("Number of Events");

hJet_eem = fs->make<TH1D>("hJet_eem", "hJet_eem", 100, 0., 2000.); 
hJet_eem->GetXaxis()->SetTitle("Jet EM E (in GeV)");
hJet_eem->GetYaxis()->SetTitle("Number of Events");

hJet_ehad = fs->make<TH1D>("hJet_ehad", "hJet_ehad", 100, 0., 2000.); 
hJet_ehad->GetXaxis()->SetTitle("Jet HAD E (in GeV)");
hJet_ehad->GetYaxis()->SetTitle("Number of Events");

hJet_fhot = fs->make<TH1D>("hJet_fhot", "hJet_fhot", 50, -1, 2); 
hJet_fhot->GetXaxis()->SetTitle("Jet fhot");
hJet_fhot->GetYaxis()->SetTitle("Number of Events");

hJet_depth = fs->make<TH1D>("hJet_depth", "hJet_depth", 100, -16000, -14000); 
hJet_depth->GetXaxis()->SetTitle("Jet depth");
hJet_depth->GetYaxis()->SetTitle("Number of Events");

hJet_ntower = fs->make<TH1D>("hJet_ntower", "hJet_ntower", 16, 1, 17); 
hJet_ntower->GetXaxis()->SetTitle("Jet ntower");
hJet_ntower->GetYaxis()->SetTitle("Number of Events");

hJet_sigmaz = fs->make<TH1D>("hJet_sigmaz", "hJet_sigmaz", 100, 0, 100); 
hJet_sigmaz->GetXaxis()->SetTitle("Jet sigmaz");
hJet_sigmaz->GetYaxis()->SetTitle("Number of Events");

hJet_width = fs->make<TH1D>("hJet_width", "hJet_width", 100, 0, 50); 
hJet_width->GetXaxis()->SetTitle("Jet width");
hJet_width->GetYaxis()->SetTitle("Number of Events");



hNPV = fs->make<TH1D>("hNPV", "hNPV", 10, 0, 10); 
hNPV->GetXaxis()->SetTitle("Number of Primary Vertices");
hNPV->GetYaxis()->SetTitle("Number of Events");

hEventSelection = fs->make<TH1D>("hEventSelection", "hEventSelection", 5, 0, 5); 
hEventSelection->GetXaxis()->SetTitle("Selection cut");
hEventSelection->GetYaxis()->SetTitle("Number of Events");

hCASTOR_totalE_towers = fs->make<TH1D>("hCASTOR_totalE_towers", "hCASTOR_totalE_towers", 400, 0, 4000); 
hCASTOR_totalE_towers->GetXaxis()->SetTitle("CASTOR total energy with towers");
hCASTOR_totalE_towers->GetYaxis()->SetTitle("Number of Events");

hCASTOR_totalE_80rechits = fs->make<TH1D>("hCASTOR_totalE_80rechits", "hCASTOR_totalE_80rechits", 252, -30, 3750);
hCASTOR_totalE_80rechits->GetXaxis()->SetTitle("CASTOR total energy with 80 rechits");
hCASTOR_totalE_80rechits->GetYaxis()->SetTitle("Number of Events");

hCASTOR_totalE_allrechits = fs->make<TH1D>("hCASTOR_totalE_allrechits", "hCASTOR_totalE_allrechits", 252, -30, 3750);
hCASTOR_totalE_allrechits->GetXaxis()->SetTitle("CASTOR total energy with all rechits");
hCASTOR_totalE_allrechits->GetYaxis()->SetTitle("Number of Events");


Nevents = 0;

myPI = 3.141592653589793;

}


DemoAnalyzer::~DemoAnalyzer() {
	// do anything here that needs to be done at destruction time
	// (e.g. close files, deallocate resources etc.)
}



//
// member functions
//

// ------------ method called for each event  ------------
void DemoAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

// **********************************************
// here each relevant event will get analyzed 
// **********************************************

using namespace edm;
using namespace reco;
using namespace std;


// Event is to be analyzed

//  LogInfo("Demo")
//  << "Starting to analyze \n"
//  << "Event number: " << (iEvent.id()).event()
//  << ", Run number: " << iEvent.run()
//  << ", Lumisection: " << iEvent.luminosityBlock();

//------------------Load (relevant) Event information------------------------//
// INFO: Getting Data From an Event
// https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookChapter4#GetData
// https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideEDMGetDataFromEvent#get_ByLabel
// https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAodDataTable

  // count all events
  hEventSelection->Fill(0.,1.);

  Handle<VertexCollection> vtxcoll;
  iEvent.getByLabel("offlinePrimaryVertices",vtxcoll);

  int NGoodVtx = 0;
  for(VertexCollection::const_iterator pv = vtxcoll->begin(); pv!= vtxcoll->end(); ++pv) {
     double vtx_rho = sqrt(pv->x()*pv->x() + pv->y()*pv->y());
     //--  GoodVertex
     if(!pv->isFake() && pv->ndof() >= 4 && abs(pv->z()) <= 15 && vtx_rho <=2) NGoodVtx++;
  }

  hNPV->Fill(NGoodVtx);
  if (NGoodVtx != 1) return;

  // fill after vertex selection
  hEventSelection->Fill(1.,1.);

  // ask for activity in HF
  Handle<CaloTowerCollection> CaloTowerColl;
  iEvent.getByLabel("towerMaker",CaloTowerColl);

  bool HFplus = false;
  bool HFminus = false;
  for (CaloTowerCollection::const_iterator iCT = CaloTowerColl->begin() ; iCT != CaloTowerColl->end() ; ++iCT) {
    bool hasHF = false;
    //-- loop over CaloTower constituents
    for(size_t iconst = 0; iconst < iCT->constituentsSize(); iconst++) {
      DetId detId = iCT->constituent(iconst);
      if(detId.det()==DetId::Hcal) {
        HcalDetId hcalDetId(detId);
        if(hcalDetId.subdet()==HcalForward) hasHF = true;
      } 
    }
    if (hasHF && iCT->energy() > 4. && iCT->zside() == 1 && iCT->eta() > 3.23 && iCT->eta() < 4.65) HFplus = true;
    if (hasHF && iCT->energy() > 4. && iCT->zside() == -1 && iCT->eta() < -3.23 && iCT->eta() > -4.65) HFminus = true;
  }

  if (!HFplus || !HFminus) return;

  // fill after HF selection
  hEventSelection->Fill(2.,1.);

  // ask for activity in CASTOR - using towers
  edm::Handle<CastorTowerCollection> towercoll;
  iEvent.getByLabel("CastorTowerReco",towercoll);
  // ask at least 1 tower above noise threshold
  if (towercoll->size() == 0) return;

  // fill after CASTOR selection
  hEventSelection->Fill(3.,1.);

  // count events that passed all cuts
  Nevents++;


  // start with filling histograms of different objects

  // acces the CASTOR rechits
  Handle<CastorRecHitCollection> rechitcoll;
  iEvent.getByLabel("rechitcorrector",rechitcoll);

  //-- loop over the rechit collection
  if(rechitcoll.isValid()) {
		double total_80rechit_energy = 0.0;
		double total_allrechit_energy = 0.0;
	    for(size_t i = 0; i < rechitcoll->size(); ++i) {
			const CastorRecHit & rh = (*rechitcoll)[i];
			HcalCastorDetId castorid = rh.id();
			double myRHenergy = rh.energy();
			
			hRecHit_map->Fill(castorid.sector(),castorid.module());
			if (myRHenergy > 0.65) hRecHit_occupancy->Fill(castorid.sector(),castorid.module());
			hRecHit_module->Fill(castorid.module(),myRHenergy);
			hRecHit_sector->Fill(castorid.sector(),myRHenergy);
            int rh_channel = 16*(castorid.module()-1) + castorid.sector();
			hRecHit_channel->Fill(rh_channel,myRHenergy);
			hRecHit_energy->Fill(myRHenergy);
            if (rh_channel <= 80) {
				hRecHit_5Msector->Fill(castorid.sector(),myRHenergy);
				total_80rechit_energy += myRHenergy;
			}
			total_allrechit_energy += myRHenergy;
		}
        hCASTOR_totalE_80rechits->Fill(total_80rechit_energy);
		hCASTOR_totalE_allrechits->Fill(total_allrechit_energy);
		
  }

  
  // access the CASTOR towers

  if(towercoll.isValid()) {

    hTower_multi->Fill(towercoll->size());

    double totalenergy = 0.0;
    double leadingtowerenergy = 0.0;
    for(unsigned int i=0;i<towercoll->size();i++) {

      const CastorTower & castortower = (*towercoll)[i];
      double myTOWenergy = castortower.energy();

      hTower_energy->Fill(myTOWenergy);
      hTower_phi->Fill(castortower.phi());
      hTower_fem->Fill(castortower.fem());
      hTower_eem->Fill(castortower.emEnergy());
      hTower_ehad->Fill(castortower.hadEnergy());
      hTower_depth->Fill(castortower.depth());
      hTower_fhot->Fill(castortower.fhot());
      hTower_ncell->Fill(castortower.rechitsSize());
      
      if (myTOWenergy > leadingtowerenergy) leadingtowerenergy = myTOWenergy;
      totalenergy += myTOWenergy;	
    }
    hCASTOR_totalE_towers->Fill(totalenergy);
    hLTower_energy->Fill(leadingtowerenergy);
  }


  // access the CASTOR jets
  edm::Handle<edm::View< reco::BasicJet > > basicjetcoll;  //-- uncorrected jets
  edm::Handle<reco::CastorJetIDValueMap> jetIdMap;

  iEvent.getByLabel("ak5BasicJets",basicjetcoll);
  iEvent.getByLabel("ak5CastorJetID",jetIdMap);

  if(basicjetcoll.isValid()) {

    for(edm::View<reco::BasicJet>::const_iterator ibegin = basicjetcoll->begin(), iend = basicjetcoll->end(), ijet = ibegin; ijet != iend; ++ijet) {

      unsigned int idx = ijet - ibegin;
      const BasicJet & basicjet = (*basicjetcoll)[idx];
      
      double myJETenergy = basicjet.energy();
	  
      hJet_energy->Fill(myJETenergy);
      hJet_phi->Fill(basicjet.phi());

      edm::RefToBase<reco::BasicJet> jetRef = basicjetcoll->refAt(idx);
      reco::CastorJetID const & jetId = (*jetIdMap)[jetRef];

      hJet_fem->Fill(jetId.fem);
      hJet_eem->Fill(jetId.emEnergy);
      hJet_ehad->Fill(jetId.hadEnergy);

      hJet_width->Fill(jetId.width*(180/myPI)); // convert from radians to degrees
      hJet_depth->Fill(jetId.depth);
      hJet_fhot->Fill(jetId.fhot);
      hJet_sigmaz->Fill(jetId.sigmaz);
      hJet_ntower->Fill(jetId.nTowers);
      
      // perform jet noncompensation calibration
      // select hadronic jet
      bool HAD = true;
      if (jetId.depth > -14450 && myJETenergy < 175) HAD = false;
      if (jetId.depth > -14460 && myJETenergy > 175) HAD = false;
      if (jetId.fem > 0.95) HAD = false;
      
      // select EM jet
      bool EM = true;
      if (jetId.fhot < 0.45) EM = false;
      if (jetId.fem < 0.90) EM = false;
      if (jetId.sigmaz > 30 && myJETenergy < 75) EM = false;
      if (jetId.sigmaz > 40 && myJETenergy > 75) EM = false;
      if (jetId.width*(180/myPI) > 11.5) EM = false; // convert from radians to degrees
      if (jetId.depth < -14450 && myJETenergy < 125) EM = false;
      if (jetId.depth < -14460 && myJETenergy > 125) EM = false;     
      
      // calibrate only hadronic jets
      if (HAD) {
		// apply calibration factors
		double Ecal = 0.0;
		if (basicjet.phi() > 4*(myPI/8) && basicjet.phi() < 5*(myPI/8)) {
			// include different sectors 5 for Commissioning10 data were first channels are removed
			/*if ( iEvent.eventAuxiliary().isRealData())*/ Ecal = myJETenergy*(1.3 + 0.23*log(-149 + myJETenergy)); // data (SL) 
			//if (!iEvent.eventAuxiliary().isRealData()) Ecal = myJETenergy*(0.9 + 0.25*log(-149 + myJETenergy)); // MC (FS) 
		} else if (basicjet.phi() > 5*(myPI/8) && basicjet.phi() < 6*(myPI/8)) {
			// include different sectors 6 for Commissioning10 data were first channels are removed
			/*if ( iEvent.eventAuxiliary().isRealData())*/ Ecal = myJETenergy*(1.4 + 0.21*log(-149 + myJETenergy)); // data (SL) 
			//if (!iEvent.eventAuxiliary().isRealData()) Ecal = myJETenergy*(-5.8 + 1.3*log(144 + myJETenergy)); // MC (FS)  
		} else {
			/*if ( iEvent.eventAuxiliary().isRealData())*/ Ecal = myJETenergy*(1.8 + 0.0037*log(1 + myJETenergy)); // data (SL) good sectors
			//if (!iEvent.eventAuxiliary().isRealData()) Ecal = myJETenergy*(1.5 + 0.0024*log(1 + myJETenergy)); // MC (FS) good sectors
			
		}
		hJet_calenergy->Fill(Ecal); // fill with calibrated HAD jet
	  } else {
		hJet_calenergy->Fill(myJETenergy); // fill with other jets
	  }

    }
  }



} //DemoAnalyzer::analyze ends


// ------------ method called once each job just before starting event loop  ------------
void DemoAnalyzer::beginJob() {

}

// ------------ method called once each job just after ending the event loop  ------------
void DemoAnalyzer::endJob() {

  std::cout << " number of events that passed selection cuts: " << Nevents << std::endl;
  
  

}

//define this as a plug-in
DEFINE_FWK_MODULE(DemoAnalyzer);


