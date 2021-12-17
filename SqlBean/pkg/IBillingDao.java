package pkg;

import java.sql.Timestamp;
import java.util.List;

import pkg.dto.PoBillingMaster;
import pkg.dto.PoBillingStatus;

public interface IBillingDao {
	PoBillingMaster selectPoBillingMasterByBillingId(String billingId) throws Exception;

	PoBillingStatus selectPoBillingStatusByLoginId(String loginId) throws Exception;

	void insertPoBillingStatus(PoBillingStatus poBillingStatus) throws Exception;

	void updatePoBillingStatusWhenStatusCreated(PoBillingStatus poBillingStatus, List<Integer> billingStatusList) throws Exception;

	void updatePoBillingStatusWhenStatusRecovered(PoBillingStatus poBillingStatus) throws Exception;

	void updatePoBillingStatusWhenStatusChanged(PoBillingStatus poBillingStatus) throws Exception;

	void updatePoBillingStatusWhenStatusChangedOrErrorNoUpdateDateInWhere(PoBillingStatus poBillingStatus) throws Exception;

	void updatePoBillingStatusWhenStatusChangedNoUpdateDateInWhere(PoBillingStatus poBillingStatus) throws Exception;

	void updatePoBillingStatusWhenRecovery(PoBillingStatus poBillingStatus) throws Exception;

	void deletePoBillingStatusByStatusAndUpdateDate(String loginId, int[] billingStatus, Timestamp updateDate) throws Exception;

	List<PoBillingStatus> selectPoBillingStatusForRecovery() throws Exception;
}